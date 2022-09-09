from .detRes import DetRes
from pathlib import Path
from dataclasses import dataclass, field
from typing import List
import math

@dataclass
class SourceProps:
    energy: float = 0.0
    energy_unit: str = ""

@dataclass
class GeomProps:
    distance: float = None
    angle: float = None

@dataclass
class DetectorProps:
    src_props: SourceProps = None
    quantity: str = ""
    num: str = "" # because for 2d matrix detector num could be '3-11' that means that it's 3d column and 11-th row etc.
    geom_props: GeomProps = None
    __tags: List[str] = None

    def __post_init__(self):
        if self.src_props is None:
            self.src_props = SourceProps()
        self.__tags = list()
        self.geom_props = GeomProps()
    
    def __str__(self):
        return self.getKeyname({})
        # tagstring = "-".join(self.__tags)
        # return f"{self.quantity}_{tagstring}-{self.num}_SRC[{self.src_props.energy:.2f} {self.src_props.energy_unit}]"

    def getKeyname(self, blocked : set):
        """
            *blocked contain blocked parts to form a keyword
            possible words:
                - quantity
                - energy
                - num
            **tags contain blocked tags
                tags = ['tag1', 'tag2', 'tag3']
        """
        # parts for keyname:
        parts = []
        quantity = self.quantity if 'quantity' not in blocked else ""
        parts.append(quantity)
        # bl_tags = blocked_tags['tags'] if 'tags' in blocked_tags else []
        tagstring = "-".join([tag for tag in self.__tags if tag not in blocked])
        parts.append(tagstring)
        num = self.num if 'num' not in blocked else ""
        parts.append(num)
        source = f"SRC[{self.src_props.energy:.2f} {self.src_props.energy_unit}]" if 'energy' not in blocked else ""
        parts.append(source)
        # filter parts
        parts = [i for i in parts if i]
        return "_".join(parts)

    def setTag(self, tag):
        # if self.__tags == None:
        #     self.__tags = list()
        if tag not in self.__tags:
            self.__tags.append(tag)

    def getTags(self):
        return self.__tags

class Detector:
    @staticmethod
    def createName(detprops: DetectorProps):
        return f"{detprops}"

    def __init__(self, det_props: DetectorProps = None):
        if det_props is None:
            self.detProps : DetectorProps = DetectorProps()
        else:
            self.detProps : DetectorProps = det_props
        self.prima_results : List[DetRes] = [] # Contains only primary results, which were read from files on disk
        self.wrong_results = []
        self.addit_results = [] # Contains merge versions of results, different bins versions and other, links to primary
        self.hl_res = None 

    def appendResult(self, filename):
        dr = DetRes(self.createName(self.detProps))
        try:
            dr.readDataFromCSV(filename)
        except Exception as e:
            # print(f"Can't read result from the file {Path(filename).name}, inner data is wrong\n{e}")
            dr.clear()
            self.wrong_results.append(filename)
            return
        dr.calculateStatistics()
        self.prima_results.append(dr)

    def createFromFile(self, filename):
        """
            Create detector from file
        """
        with open(filename, 'r') as f:
            f.readline() # skip 1st line
            self.detProps.quantity = f.readline().split()[1]
            self.detProps.num = f.readline().split()[1] # remember that num is a string
            for tag in f.readline().split()[1:]:
                self.detProps.setTag(tag)
            f.readline() # skip geometry line
            self.detProps.geom_props.distance = float( f.readline().split()[1] )
            self.detProps.geom_props.angle    = float( f.readline().split()[1] )
            f.readline() # skip source line
            energy_info = f.readline().split()
            self.detProps.src_props.energy = float( energy_info[1] )
            self.detProps.src_props.energy_unit = energy_info[2]
            for _ in range(5): # skip 5 lines
                f.readline()
            # detRes info is coming
            name = ' '.join(f.readline().split()[1:])
            if name != self.createName(self.detProps):
                print(f"Name problems {name} vs {self.createName(self.detProps)}")
            assert name == self.createName(self.detProps), "check for name in file and resulting name are the same"
            dr = DetRes(name)
            words = f.readline().split()
            while(words[0] != 'Histories:'): # skip the origin sequence, remain it in file for now
                words = f.readline().split()
            dr_nhists = int( float(words[1]) )
            dr_ovf_bot = float( f.readline().split()[1] )
            dr_ovf_top = float( f.readline().split()[1] )
            f.readline() # skip data header
            table_len = len(f.readline().split())
            line_len = table_len
            dr_bins = []
            dr_y = []
            dr_y2 = []
            dr_bins.append(float( f.readline().split()[0] )) # line contain the 1st bin and the other data are zeroes
            words = f.readline().split()
            while(line_len == table_len):
                words = [float(word) for word in words]
                dr_bins.append(words[0])
                dr_y.append(words[1])
                dr_y2.append(words[2])

                words = f.readline().split()
                line_len = len(words)
            # the file reading is finished
            dr.setData(
                nhists=dr_nhists,
                overflow_bot=dr_ovf_bot,
                overflow_top=dr_ovf_top,
                bins=dr_bins,
                y=dr_y,
                y2=dr_y2,
                origin=f"READ: {filename}"
            )
            dr.calculateStatistics()
            self.prima_results.append(dr)

    def mergeResults(self):
        dr = DetRes(self.createName(self.detProps))
        for res in self.prima_results:
            dr.appendData(res)
        self.addit_results.append(dr)

    def dump_to_file(self, dr: DetRes, filename: str):
        res = "DETECTOR_HEADER\n"
        res += f"Quantity: {self.detProps.quantity}" + "\n"
        res += f"Det_num: {self.detProps.num}" + "\n"
        res += f"Tags: {' '.join(self.detProps.getTags())}" + "\n"
        res += " GEOMETRY\n"
        res += f"Distance: {self.detProps.geom_props.distance}" + "\n"
        res += f"Angle: {self.detProps.geom_props.angle}" + "\n"
        res += " SOURCE:\n"
        res += f"Energy: {self.detProps.src_props.energy} {self.detProps.src_props.energy_unit}" + "\n"
        res += " RESULTS:\n"
        res += f"Num_of_prima_results: {len(self.prima_results)}" + "\n"
        res += f"Num_of_wrong_results: {len(self.wrong_results)}" + "\n"
        res += f"Num_of_addit_results: {len(self.addit_results)}" + "\n"
        res += dr.printData()
        with open(filename, 'w') as out:
            out.write(res)

    # methods to get several data for plots
    def highlightResult(self, dr: DetRes):
        self.hl_res = dr
        if not self.hl_res.stat.has_calculated:
            self.hl_res.calculateStatistics()

    # next methods apply to hl result
    def get_means_hl(self):
        # TODO change y and y2 and other data to start with 0 for all of them
        return self.hl_res.BINS[self.hl_res.bin_index],\
            [0] + self.hl_res.stat.means,\
            [0] + self.hl_res.stat.lover_bound,\
            self.hl_res.stat.upper_bound + [0]

    def get_norm_hl(self): # sum = 1
        s = sum(self.hl_res.y)
        res = [0]
        for item in self.hl_res.y:
            res.append(item/s)
        return self.hl_res.BINS[self.hl_res.bin_index], res

    def get_norm_width_hl(self):
        s = sum(self.hl_res.y)
        res = [0]
        for i in range(len(self.hl_res.y)):
            width = self.hl_res.BINS[self.hl_res.bin_index][i+1] - self.hl_res.BINS[self.hl_res.bin_index][i]
            res.append(self.hl_res.y[i]/s/width)
        return self.hl_res.BINS[self.hl_res.bin_index], res
        
    def get_norm_width_theta_hl(self):
        s = sum(self.hl_res.y)
        res = [0]
        for i in range(len(self.hl_res.y)):
            theta1 = self.hl_res.BINS[self.hl_res.bin_index][i]
            theta2 = self.hl_res.BINS[self.hl_res.bin_index][i+1]
            omega = 2*math.pi*(math.cos(theta1*math.pi/180.0) - math.cos(theta2*math.pi/180.0))
            res.append(self.hl_res.y[i]/s/omega)
        return self.hl_res.BINS[self.hl_res.bin_index], res

    def get_norm_width_phi_hl(self):
        s = sum(self.hl_res.y)
        res = [0]
        for i in range(len(self.hl_res.y)):
            phi_1 = self.hl_res.BINS[self.hl_res.bin_index][i]
            phi_2 = self.hl_res.BINS[self.hl_res.bin_index][i+1]
            omega = (phi_2 - phi_1) * math.pi/180.0 * 2
            res.append(self.hl_res.y[i]/s/omega)
        return self.hl_res.BINS[self.hl_res.bin_index], res