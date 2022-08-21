from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from anadet.detectorManager import DetectorManager
from anadet.filesManager import FilesManager


data_dir = "C:/Projects/room/build-src-room-Desktop_Qt_5_15_0_MSVC2019_64bit-Release"
results_dir = "C:/Projects/room/results"


if __name__ == "__main__":
    fm = FilesManager()
    fm.readDirectory(data_dir)
    detector_filenames = fm.getDetFiles()
    # for df in detector_filenames:
    #     print(df)
    dm = DetectorManager()
    for filename in detector_filenames:
        dm.appendResults(str(filename))
    for detkey in dm.detectors:
        print(f"{detkey}  :  {len(dm.detectors[detkey].prima_results)}")
        dm.detectors[detkey].mergeResults()
        dm.detectors[detkey].addit_results[0].dumpToFile(str(Path(results_dir).joinpath(detkey+'.txt')))


    
