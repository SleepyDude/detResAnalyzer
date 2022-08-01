from pathlib import Path

class Crawler:
    IGNORE_ITEMS = ["__pycache__", ".DS_Store"]
    def __init__(self, root):
        self.root_dir = Path(root)

    def getFiles(self):
        return self._getFiles(self.root_dir)

    def _getFiles(self, dir: Path):
        filelist = []
        for item in dir.iterdir():
            if item.name in self.IGNORE_ITEMS:
                continue
            if item.is_file():
                filelist.append(str(item.resolve()))
            else:
                filelist.extend(self._getFiles(item))
        return filelist



        
