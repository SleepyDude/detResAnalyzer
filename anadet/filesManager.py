from anadet.crawler import Crawler

class FilesManager:
    def __init__(self):
        self.detectors = []
        self.metaFiles = []

    def readDirectory(self, dir):
        cr = Crawler(dir)
        files = cr.getFiles()
        for file in files:
            if file.endswith('.csv'):
                self.detectors.append(file)
            elif 'meta' in file:
                self.metaFiles.append(file)