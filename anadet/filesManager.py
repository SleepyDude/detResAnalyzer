from anadet.crawler import Crawler

class FilesManager:
    def __init__(self):
        self.detectorFiles = []
        self.metaFiles = []

    def readDirectory(self, dir):
        cr = Crawler(dir)
        files = cr.getFiles()
        for file in files:
            if file.name.endswith('.csv'):
                self.detectorFiles.append(file)
            elif file.name.endswith('meta.yaml'):
                self.metaFiles.append(file)

    def getDetFiles(self):
        return self.detectorFiles

    def getMetaFiles(self):
        return self.metaFiles