from os import environ

from ..anadet.detectorManager import DetectorManager
from ..anadet.filesManager import FilesManager
from ..anadet.detectorUtils import prep_dets_for_filtering

# *** READ REAL DATA ***
fm = FilesManager()
data_dir = environ.get('ANADET_RESULT')
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

detectors = prep_dets_for_filtering(dm.detectors)