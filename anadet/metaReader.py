import yaml
from pprint import pprint as pp

class MetaReader:

    def readFile(self, filename):
        with open(filename) as f:
            data = yaml.safe_load(f)
            self.data = data

    def getParamsForDetector(self, detType: str, detNum: int): # TODO: tags system
        head = self.data[detType]['__Table'][0]
        data = self.data[detType]['__Table'][detNum]
        return {
            head[1] : data[1],
            head[2] : data[2],
        }
