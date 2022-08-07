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
        self.results = []