from anadet.crawler import Crawler

class FilesManager:
    def __init__(self):
        self.detectorFiles = []
        self.metaFiles = []

    def readDirectory(self, dir):
        cr = Crawler(dir)
        files = cr.getFiles()
        for file in files:
            if file.endswith('.csv'):
                self.detectorFiles.append(file)
            elif 'meta' in file:
                self.metaFiles.append(file)

    def getDetFiles(self):
        return self.detectorFiles