import math
from anadet.dataSearcher import DataSearcher

class CSVHeaderError(Exception):
    ...

class CSVReadError(Exception):
    ...

class AppendResError(Exception):
    ...

class DetResult:
    """
        self.merge_list = filenames of datafiles, which were appended to this result object 
    """
    START_DATA_IDX = 7
    BINS = [] # some results share the same bin sequence

    def __init__(self, name=''):
        self.name = name
        self.clear()

    def readDataFromCSV(self, filename):
        ds = DataSearcher()
        self.nhists = ds.lookingForNhists(filename)
        self.filename = filename
        self.merge_list.append(filename)
        # Method shouldn't handle exceptions, just raise them
        with open(self.filename, 'r') as f:
            # Reading header
            header = list()
            for _ in range(self.START_DATA_IDX):
                header.append(f.readline().strip())
            self.processHeader(header) # could throw an exception
            # Reading bottom overflow
            self.overflow_bot = float(f.readline().strip().split(',')[1]) # Sw
            # Reading data
            self.y = []
            self.y2 = []
            for _ in range(self.data_size):
                line = f.readline().strip()
                if not line:
                    continue # case of empty strings at the end of the file
                items = list(map(float, line.split(',')))
                if len(items) != 5:
                    raise CSVReadError("ERROR: looks like the data in file doesn't fit the header")
                self.y.append(items[1])
                self.y2.append(items[2])
            # Reading top overflow
            self.overflow_top = float(f.readline().strip().split(',')[1]) # Sw

    def processHeader(self, header: list):
        if header[0] != "#class tools::histo::h1d":
            raise CSVHeaderError("HEADER ERROR: we expect tools::histo::h1d file")
        self.title = header[1][7:].strip()
        axis = header[3].split()
        bins = None
        if axis[1] == 'edges':
            bins = [float(it) for it in axis[2:]]
        elif axis[1] == 'fixed':
            dx = (float(axis[4]) - float(axis[3])) / int(axis[2])
            bins = [float(axis[3]) + dx * i for i in range(int(axis[2]) + 1)]
        else:
            raise CSVHeaderError(f"HEADER ERROR: axis type should be 'edges' of 'fixed', but '{axis[1]}' got")
        self.bin_index = self.getBinsIndex(bins)
        self.data_size = int(header[5].split()[1]) - 2

    @classmethod
    def getBinsIndex(cls, abins):
        #looking for exact the same bins
        for i in range(len(cls.BINS)):
            if len(cls.BINS[i]) != len(abins):
                continue
            for pair in zip(cls.BINS[i], abins):
                if not math.isclose(pair[0], pair[1], rel_tol=1e-4):
                    continue
            # If we here - we found bins
            return i
        # We are not found the same bins, so we append a new and return it's index
        cls.BINS.append(abins)
        return len(cls.BINS)-1

    def clear(self):
        self.y = []
        self.y2 = []
        self.merge_list = list()
        self.overflow_bot = 0
        self.overflow_top = 0
        self.data_size = 0
        self.bin_index = None
        self.title = ""
        self.nhists = 0

    def appendData(self, other):
        if len(self.y) == 0: # append data to the new result object, need to prepare data structures to fit the other data
            self.data_size = other.data_size
            self.bin_index = other.bin_index
            self.y  = [0.0 for _ in other.y]
            self.y2 = [0.0 for _ in other.y2]
        
        if self.bin_index != other.bin_index:
            raise AppendResError(f"MERGE ERROR: can't merge detResults with different bins")
        if self.data_size != other.data_size:
            raise AppendResError(f"MERGE ERROR: can't merge detResults with different sizes {self.data_size} vs {other.data_size}")
        # appending data
        self.title = "Merged"
        self.filename = "Merged"
        self.merge_list.append(other.filename)
        self.overflow_bot += other.overflow_bot
        self.overflow_top += other.overflow_top
        self.nhists += other.nhists
        for i in range(self.data_size):
            self.y[i] += other.y[i]
            self.y2[i] += other.y2[i]

    def calculateStatistics(self):
        # TODO - need to make a state system - statistic calculate makes sence only after we deal with results object with data inside
        self.M = [i/self.nhists for i in self.y]
        self.D = [ self.y2[i]/(self.nhists-1) - self.y[i]*self.y[i]/(self.nhists-1)/(self.nhists) for i in range(self.data_size) ]
        self.sigma = [math.sqrt(Di/self.nhists) for Di in self.D]
        self.delta = [self.sigma[i]/self.M[i] for i in range(self.data_size)]