import math
from anadet.dataSearcher import DataSearcher

class DetRes:
    """
        Class for Detector Results
        Represents 1-dim histogram with data
            cls.BINS = List(List(float)) - contains edges (x-axis of data), num_of_edges = num_of_data + 1
                data:
            self.y = List(float): hist data
            self.y2 = List(float): hist data^2
            self.overflow_bot = float
            self.overflow_top = float
            self.bin_index = int: len(cls.BINS[self.bin_index]) - 1 == len(self.y) == len(self.y2)
            self.nhists = int: num of histories which fit the results
                meta info:
            self.origin_sequence = List(str)

    """
    class CSVHeaderError(Exception):
        ...

    class CSVReadError(Exception):
        ...

    class AppendResError(Exception):
        ...

    BINS = [] # some results share the same bin sequence

    def __init__(self, name=''):
        self.name = name # detector related info as a name
        self.clear()

    def clear(self):
        # data
        self.y = []
        self.y2 = []
        self.overflow_bot = 0
        self.overflow_top = 0
        self.bin_index = None
        self.nhists = 0
        # other
        self.origin_sequence = []

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

    def __str__(self):
        if len(self.origin_sequence):
            return f"<DetRes {self.name} origin={self.origin_sequence[-1]}>"
        else:
            return f"<DetRes {self.name} EMPTY DATA>"

    def readDataFromCSV(self, filename):
        START_DATA_IDX = 7
        if not self.nhists:
            ds = DataSearcher()
            self.nhists = ds.lookingForNhists(filename)
            if not self.nhists:
                raise Exception(f'ERROR NHISTS: could not find num of histories in {filename}, set it previously of put it into the filename')
        # Method shouldn't handle exceptions, just raise them
        with open(filename, 'r') as f:
            # Reading header
            header = list()
            for _ in range(START_DATA_IDX):
                header.append(f.readline().strip())
            data_size = self.processCSVHeader(header) # could throw an exception
            # Reading bottom overflow
            self.overflow_bot = float(f.readline().strip().split(',')[1]) # Sw
            # Reading data
            self.y = []
            self.y2 = []
            for _ in range(data_size):
                line = f.readline().strip()
                print(line)
                if not line:
                    continue # case of empty strings at the end of the file
                items = list(map(float, line.split(',')))
                if len(items) != 5:
                    raise self.CSVReadError("ERROR: looks like the data in file doesn't fit the header")
                self.y.append(items[1])
                self.y2.append(items[2])
            # Reading top overflow
            self.overflow_top = float(f.readline().strip().split(',')[1]) # Sw
        self.origin_sequence.append(f"READ: {filename}")
    
    def processCSVHeader(self, header: list) -> int:
        if header[0] != "#class tools::histo::h1d":
            raise self.CSVHeaderError("HEADER ERROR: we expect tools::histo::h1d file")
        axis = header[3].split()
        bins = None
        if axis[1] == 'edges':
            bins = [float(it) for it in axis[2:]]
        elif axis[1] == 'fixed':
            dx = (float(axis[4]) - float(axis[3])) / int(axis[2])
            bins = [float(axis[3]) + dx * i for i in range(int(axis[2]) + 1)]
        else:
            raise self.CSVHeaderError(f"HEADER ERROR: axis type should be 'edges' of 'fixed', but '{axis[1]}' got")
        self.bin_index = self.getBinsIndex(bins)
        data_size = int(header[5].split()[1]) - 2
        return data_size

    def appendData(self, other: 'DetRes'):
        if len(self.y) == 0: # append data to the new result object, need to prepare data structures to fit the other data
            self.bin_index = other.bin_index
            self.y  = [0.0 for _ in other.y]
            self.y2 = [0.0 for _ in other.y2]
        if self.bin_index != other.bin_index:
            raise self.AppendResError(f"APPEND ERROR: can't append data with different bins")
        if len(self.y) != len(other.y):
            raise self.AppendResError(f"APPEND ERROR: can't append data with different sizes {len(self.y)} vs {len(other.y)}")
        # appending data
        self.origin_sequence.append(f"APPEND: {other}")
        self.overflow_bot += other.overflow_bot
        self.overflow_top += other.overflow_top
        self.nhists += other.nhists
        for i in range(len(self.y)):
            self.y[i] += other.y[i]
            self.y2[i] += other.y2[i]

    def calculateStatistics(self):
        # TODO - need to make a state system - statistic calculate makes sence only after we deal with results object with data inside
        self.M = [i/self.nhists for i in self.y]
        self.D = [ self.y2[i]/(self.nhists-1) - self.y[i]*self.y[i]/(self.nhists-1)/(self.nhists) for i in range(len(self.y)) ]
        self.sigma = [math.sqrt(Di/self.nhists) for Di in self.D]
        self.delta = [self.sigma[i]/self.M[i] for i in range(len(self.y))]
