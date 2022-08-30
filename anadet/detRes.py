from cmath import isclose
from dataclasses import dataclass
import math
from anadet.dataSearcher import DataSearcher
from pathlib import Path
from typing import List
from dataclasses import dataclass, field

@dataclass
class StatisticData:
    nhists: int
    means: List[float] = None
    variances: List[float] = None
    st_devs: List[float] = None # sigma
    deltas: List[float] = None
    lover_bound: List[float] = None
    upper_bound: List[float] = None
    # some params
    delta_min: float = math.inf
    delta_max: float = -math.inf
    has_calculated: bool = False

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
    
    @staticmethod
    def calcVar(y: float, y2: float, nhists: int):
        if nhists <= 1:
            print("Warning: nhists <= 1")
            return 0
        return y2/(nhists-1) - y*y/(nhists-1)/nhists

    @staticmethod
    def calcDelta(y: float, y2: float, nhists: int):
        if math.isclose(y, 0, abs_tol=1e-14):
            return 0
        var = DetRes.calcVar(y, y2, nhists)
        sigma = math.sqrt(var / nhists)
        M = y / nhists
        return sigma / M

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
        # statistic
        self.stat = StatisticData(nhists=0)
        # other
        self.origin_sequence = []
        self.state = dict()

    @classmethod
    def getBinsIndex(cls, abins):
        #looking for exact the same bins
        for i in range(len(cls.BINS)):
            if len(cls.BINS[i]) != len(abins):
                continue
            bins_found = True
            for pair in zip(cls.BINS[i], abins):
                if not math.isclose(pair[0], pair[1], rel_tol=1e-4):
                    bins_found = False
                    break
            # If we here - we found bins
            if bins_found:
                return i
        # We are not found the same bins, so we append a new and return it's index
        cls.BINS.append(abins)
        return len(cls.BINS)-1

    def __str__(self):
        if len(self.origin_sequence):
            seq_string = '\n'.join(self.origin_sequence)
            return f"<DetRes({self.name})origin={seq_string}>"
        else:
            return f"<DetRes({self.name})EMPTY DATA>"

    def readDataFromCSV(self, filename):
        START_DATA_IDX = 7
        if not self.stat.nhists:
            ds = DataSearcher()
            self.stat.nhists = ds.lookingForNhists(filename)
            if not self.stat.nhists:
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
                if not line:
                    continue # case of empty strings at the end of the file
                items = list(map(float, line.split(',')))
                if len(items) != 5:
                    raise self.CSVReadError("ERROR: looks like the data in file doesn't fit the header")
                self.y.append(items[1])
                self.y2.append(items[2])
            # Reading top overflow
            self.overflow_top = float(f.readline().strip().split(',')[1]) # Sw
        self.origin_sequence.append(f"READ: {Path(filename).as_posix()}")
    
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
        self.stat.nhists += other.stat.nhists
        for i in range(len(self.y)):
            self.y[i] += other.y[i]
            self.y2[i] += other.y2[i]

    def calculateStatistics(self):
        # TODO - need to make a state system - statistic calculate makes sence only after we deal with results object with data inside
        self.stat.means = [i/self.stat.nhists for i in self.y]
        self.stat.variances = [ self.calcVar(self.y[i], self.y2[i], self.stat.nhists) for i in range(len(self.y)) ]
        self.stat.st_devs = [math.sqrt(Di/self.stat.nhists) for Di in self.stat.variances]
        # upper and lower bounds for graphic plot
        self.stat.lover_bound = [self.stat.means[i] - self.stat.st_devs[i] for i in range(len(self.y))]
        self.stat.upper_bound = [self.stat.means[i] + self.stat.st_devs[i] for i in range(len(self.y))]
        # TODO - zero division problem, need to indicate, is the value a zero or just a small value
        self.stat.deltas = [0.0 for _ in range(len(self.y))]
        for i in range(len(self.y)):
            if not math.isclose(self.stat.means[i], 0, abs_tol=1e-14):
                self.stat.deltas[i] = self.stat.st_devs[i]/self.stat.means[i]
                if self.stat.deltas[i] > self.stat.delta_max:
                    self.stat.delta_max = self.stat.deltas[i]
                if self.stat.deltas[i] < self.stat.delta_min:
                    self.stat.delta_min = self.stat.deltas[i]
        self.stat.has_calculated = True

    def setData(self, **data):
        if  'y' not in data or\
            'y2' not in data or\
            'bins' not in data or\
            'overflow_top' not in data or\
            'overflow_bot' not in data or\
            'nhists' not in data or\
            'origin' not in data:
            raise Exception(f'ERROR DetRes.setData: Wrong data format {data}')
        # TODO - maybe add some data validation
        self.y = data['y']
        self.y2 = data['y2']
        self.overflow_bot = data['overflow_bot']
        self.overflow_top = data['overflow_top']
        self.stat.nhists = data['nhists']
        self.origin_sequence.append(data['origin'])
        self.bin_index = self.getBinsIndex(data['bins'])
        self.stat.has_calculated = False

    def createChild(self, abins: List[float]) -> 'DetRes':
        chd_y = [0.0 for _ in range(len(abins) - 1)]
        chd_y2 = [0.0 for _ in range(len(abins) - 1)]
        chd_ovf_top = self.overflow_top
        chd_ovf_bot = self.overflow_bot

        # start positions
        bin_i = 1
        chd_bin_i = 1
        left_cut = self.BINS[self.bin_index][bin_i-1]

        while bin_i < len(self.BINS[self.bin_index]) and\
              chd_bin_i < len(abins):
            if abins[chd_bin_i] <= self.BINS[self.bin_index][bin_i-1]:
                chd_bin_i += 1 # go to next child bin
                continue
            if self.BINS[self.bin_index][bin_i] <= abins[chd_bin_i-1]:
                chd_ovf_bot += self.y[bin_i-1]
                bin_i += 1 # go to next self bin
                left_cut = self.BINS[self.bin_index][bin_i-1]
                continue
            # now two bins intersect each other
            if abins[chd_bin_i-1] > self.BINS[self.bin_index][bin_i-1] and chd_bin_i == 1: # first bin, so we will append overflow_bot
                part = (abins[chd_bin_i-1] - left_cut) / (self.BINS[self.bin_index][bin_i] - self.BINS[self.bin_index][bin_i-1])
                chd_ovf_bot += part * self.y[bin_i-1]
                left_cut = abins[chd_bin_i-1]
            
            if abins[chd_bin_i-1] > self.BINS[self.bin_index][bin_i-1]: # cases 2, 3, (5)
                left_cut = abins[chd_bin_i-1]
            # left_cut is on the place
            if abins[chd_bin_i] < self.BINS[self.bin_index][bin_i]: # cases 1, 3
                part = (abins[chd_bin_i] - left_cut) / (self.BINS[self.bin_index][bin_i] - self.BINS[self.bin_index][bin_i-1])
                chd_y[chd_bin_i-1] += part * self.y[bin_i-1]
                chd_y2[chd_bin_i-1] += part * self.y2[bin_i-1]
                left_cut = abins[chd_bin_i]
                chd_bin_i += 1 # go to next child bin
                continue
            else: # cases 2, 4
                part = (self.BINS[self.bin_index][bin_i] - left_cut) / (self.BINS[self.bin_index][bin_i] - self.BINS[self.bin_index][bin_i-1])
                chd_y[chd_bin_i-1] += part * self.y[bin_i-1]
                chd_y2[chd_bin_i-1] += part * self.y2[bin_i-1]
                bin_i += 1 # go to next self bin
                left_cut = self.BINS[self.bin_index][bin_i-1]
                continue
        while bin_i < len(self.BINS[self.bin_index]): #case when some bins remain
            part = (self.BINS[self.bin_index][bin_i] - left_cut) / (self.BINS[self.bin_index][bin_i] - self.BINS[self.bin_index][bin_i-1])
            chd_ovf_top += part * self.y[bin_i-1]
            left_cut = self.BINS[self.bin_index][bin_i]
            bin_i += 1
        chd = DetRes()
        chd.setData(y=chd_y, y2=chd_y2, overflow_bot=chd_ovf_bot, overflow_top=chd_ovf_top, nhists=self.stat.nhists, bins=abins, origin=f'CHILD from {self}')
        return chd

    def strip(self) -> 'DetRes':
        left_bin_i = 0
        right_bin_i = 1
        left_found = False
        for i in range(len(self.y)):
            if self.y[i] > 0:
                if not left_found:
                    left_found = True
                    left_bin_i = i
                right_bin_i = i+1
        chd_y = self.y[left_bin_i:right_bin_i]
        chd_y2 = self.y2[left_bin_i:right_bin_i]
        chd_ovf_bot = self.overflow_bot
        chd_ovf_top = self.overflow_top
        chd_bins = self.BINS[self.bin_index][left_bin_i:right_bin_i+1]
        chd_origin = f"STRIP from {self}"
        chd = DetRes()
        chd.setData(y=chd_y, y2=chd_y2, overflow_bot=chd_ovf_bot, overflow_top=chd_ovf_top, nhists=self.stat.nhists, bins=chd_bins, origin=chd_origin)
        return chd

    def shrinkToDelta(self, delta_max=0.1) -> 'DetRes':
        left_bin_i = 0
        right_bin_i = 0
        integral_y = 0
        integral_y2 = 0
        res_bins = []
        res_bins.append(self.BINS[self.bin_index][left_bin_i])
        for i in range(len(self.y)):
            right_bin_i += 1
            if self.y[i] == 0:
                continue # skip iteration
            integral_y += self.y[i]
            integral_y2 += self.y2[i]
            integral_delta = self.calcDelta(integral_y, integral_y2, self.stat.nhists)
            if integral_delta <= delta_max:
                res_bins.append(self.BINS[self.bin_index][right_bin_i])
                left_bin_i = right_bin_i
                integral_y = 0
                integral_y2 = 0
        if not math.isclose(res_bins[-1], self.BINS[self.bin_index][-1], abs_tol=1e-14): # we should save prev edges
            res_bins.append(self.BINS[self.bin_index][right_bin_i])
        return self.createChild(res_bins)

    def printData(self):
        if not self.stat.has_calculated:
            self.calculateStatistics()
        res = "DETRES_HEADER\n"
        res += f"Name: {self.name}" + "\n"
        # res += str(self) + "\n"
        res += f"Histories: {self.stat.nhists:.2E}" + "\n"
        res += f"Overflow_bot: {self.overflow_bot}" + "\n"
        res += f"Overflow_top: {self.overflow_top}" + "\n"
        res += "DETRES_DATA\n"
        res += "x y y2 mean mean/width norm/width delta\n"
        x = self.BINS[self.bin_index][0]
        sum_y = sum(self.y)
        norms = [i/sum_y for i in self.y]
        res += f"{x} 0 0 0 0 0 0\n"
        for i in range(len(self.y)):
            x = self.BINS[self.bin_index][i+1]
            width = self.BINS[self.bin_index][i+1] - self.BINS[self.bin_index][i]
            res += f"{x} {self.y[i]} {self.y2[i]} {self.stat.means[i]} {self.stat.means[i]/width} {norms[i]/width} {self.stat.deltas[i]}\n"
        return res

    def dumpToFile(self, filename):
        res = self.printData()
        with open(filename, 'w') as out:
            out.write(res)
        