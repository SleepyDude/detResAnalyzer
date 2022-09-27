from pathlib import Path
from typing import List

class Crawler:
    IGNORE_ITEMS = ["__pycache__", ".DS_Store"]
    def __init__(self, root):
        print(f"[*] Crawler initialization with root directory: {root}")
        self.root_dir = Path(root)

    def getFiles(self) -> List[Path]:
        return self._getFiles(self.root_dir)

    def _getFiles(self, dir: Path) -> List[Path]:
        filelist = []
        for item in dir.iterdir():
            if item.name in self.IGNORE_ITEMS:
                continue
            if item.is_file():
                filelist.append(item.resolve())
            else:
                filelist.extend(self._getFiles(item))
        return filelist
