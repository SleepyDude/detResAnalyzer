from anadet.detRes import DetRes
from pathlib import Path

class SourceProps:
    def __init__(self, energy: float, energyUnit: str):
        self.energy = energy
        self.energyUnit = energyUnit
    
    def __str__(self):
        return f"SRC:[{self.energy:.2f} {self.energyUnit}]"

class GeomProps:
    def __init__(self):
        self.wallNear = None
        self.ceilNear = None
        self.floorNear = None

class DetectorProps:
    def __init__(self, srcProps: SourceProps):
        self.srcProps = srcProps
        self.geomProps = None
        self.tags = []
        self.quantity = None

    def setTags(self, *tags):
        # TODO - prevent dublicate tags
        self.tags.extend(tags)

    def setQuantity(self, quantity):
        self.quantity = quantity


    def __str__(self):
        tagstring = "-".join(self.tags)
        return f"{self.quantity}|{tagstring}|{self.srcProps}"

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
            print(f"Can't read result from the file {Path(filename).name}, inner data is wrong\n{e}")
            dr.clear()
            self.wrong_results.append(filename)
            return
        dr.calculateStatistics()
        self.prima_results.append(dr)
