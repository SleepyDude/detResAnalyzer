from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from anadet.detectorManager import DetectorManager
from anadet.filesManager import FilesManager



# *** READ REAL DATA ***
fm = FilesManager()
data_dir = "C:/Projects/room/results"
fm.readDirectory(data_dir)
detector_filenames = fm.getDetFiles()
dm = DetectorManager()
for filename in detector_filenames:
    dm.appendResults(str(filename))

# prepare to take data from detectors
for _, det in dm.detectors.items():
    ch = det.prima_results[0].strip()
    ch = ch.shrinkToDelta(0.1)
    det.highlightResult(ch)

detectors = dm.prep_dets_for_filtering(dm.detectors)