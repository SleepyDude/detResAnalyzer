from anadet.detRes import DetRes
from pathlib import Path
from dataclasses import dataclass, field
from typing import List

@dataclass
class SourceProps:
    energy: float = None
    energy_unit: str = ""
    coordinate: List[float] = field(default_factory=list)

@dataclass
class GeomProps:
    distance: float = None
    angle: float = None

@dataclass
class DetectorProps:
    src_props: SourceProps
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

    def __init__(self, detProps):
        self.detProps = detProps
        self.prima_results = [] # Contains only primary results, which were read from files on disk
        self.wrong_results = []
        self.addit_results = [] # Contains merge versions of results, different bins versions and other, links to primary

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

    def mergeResults(self):
        dr = DetRes(self.createName(self.detProps))
        for res in self.prima_results:
            dr.appendData(res)
        self.addit_results.append(dr)


    
