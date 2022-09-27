from .crawler import Crawler

class FilesManager:
    def __init__(self):
        self.detectorFiles = []
        self.metaFiles = []

    def readDirectory(self, dir):
        if dir is None:
            raise RuntimeError('FilesManager failed to read directory. Please set directory to the "ANADET_RESULT" env')
        cr = Crawler(dir)
        files = cr.getFiles()
        for file in files:
            if file.name.endswith('.csv'):
                self.detectorFiles.append(file)
            elif file.name.endswith('meta.yaml'):
                self.metaFiles.append(file)
            elif file.name.endswith('.det.txt'):
                self.detectorFiles.append(file)

    def getDetFiles(self):
        return self.detectorFiles

    def getMetaFiles(self):
        return self.metaFiles