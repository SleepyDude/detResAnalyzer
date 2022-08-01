from pathlib import Path

class Crawler:
    IGNORE_DIRECTORIES = ["__pycache__", ".DS_Store"]
    def __init__(self, root):
        self.root_dir = Path(root)

    def getFiles(self):
        return self._getFiles(self.root_dir)

    def _getFiles(self, dir):
        filelist = []

        for item in dir.iterdir():
            if item.is_file():
                filelist.append(str(item.resolve()))
            else:
                if str(item) not in self.IGNORE_DIRECTORIES:
                    filelist.extend(self.getFiles(item))
        return filelist



        
