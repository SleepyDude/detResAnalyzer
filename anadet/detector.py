from anadet.detRes import DetRes
from pathlib import Path
from dataclasses import dataclass, field
from typing import List

@dataclass
class SourceProps:
    energy: float = 0.0
    energy_unit: str = ""
    coordinate: List[float] = field(default_factory=list)

@dataclass
class GeomProps:
    distance: float = None
    angle: float = None

@dataclass
class DetectorProps:
    src_props: SourceProps = SourceProps()
    quantity: str = ""
    num: str = "" # because for 2d matrix detector num could be '3-11' that means that it's 3d column and 11-th row etc.
    geom_props: GeomProps = None
    tags: List[str] = field(default_factory=list)
    
    def __str__(self):
        tagstring = "-".join(self.tags)
        return f"{self.quantity}_{tagstring}-{self.num}_SRC[{self.src_props.energy:.2f} {self.src_props.energy_unit}]"

class Detector:
    @staticmethod
    def createName(detprops: DetectorProps):
        return f"{detprops}"

    def __init__(self, detProps=DetectorProps()):
        self.detProps : DetectorProps = detProps
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
        pass

    def mergeResults(self):
        dr = DetRes(self.createName(self.detProps))
        for res in self.prima_results:
            dr.appendData(res)
        self.addit_results.append(dr)

    def dump_to_file(self, dr: DetRes, filename: str):
        res = "DETECTOR_HEADER\n"
        res += f"Quantity: {self.detProps.quantity}" + "\n"
        res += f"Det_num: {self.detProps.num}" + "\n"
        res += f"Tags: {' '.join(self.detProps.tags)}" + "\n"
        res += " GEOMETRY\n"
        res += f"Distance: {self.detProps.geom_props.distance}" + "\n"
        res += f"Angle: {self.detProps.geom_props.angle}" + "\n"
        res += " SOURCE:\n"
        res += f"Energy: {self.detProps.src_props.energy} {self.detProps.src_props.energy_unit}" + "\n"
        res += " RESULTS:\n"
        res += f"Num of prima_results: {len(self.prima_results)}" + "\n"
        res += f"Num of wrong_results: {len(self.wrong_results)}" + "\n"
        res += f"Num of addit_results: {len(self.addit_results)}" + "\n"
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
        return self.hl_res.BINS[self.hl_res.bin_index]