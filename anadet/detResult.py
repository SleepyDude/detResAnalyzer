import math

class CSVHeaderError(Exception):
    ...

class CSVReadError(Exception):
    ...

class DetResult:
    START_DATA_IDX = 7
    BINS = [] # some results share the same bin sequence

    def __init__(self, filename, nhists):
        self.filename = filename
        self.nhists = nhists

    def readData(self):
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
                print(line, end=' ')
                print(self.data_size)
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
            print("we expect h1 geant4 hist file")
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
        self.overflow_bot = 0
        self.overflow_top = 0
        self.data_size = 0
        self.bin_index = None
        self.title = ""