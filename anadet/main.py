from .detectorManager import DetectorManager
from .filesManager import FilesManager
from pathlib import Path

data_dir = "C:/Projects/room/build-src-room-Desktop_Qt_5_15_0_MSVC2019_64bit-Release"
results_dir = "C:/Projects/room/results"


if __name__ == "__main__":
    fm = FilesManager()
    fm.readDirectory(data_dir)
    detector_filenames = fm.getDetFiles()
    meta_filenames = fm.getMetaFiles()
    # for df in detector_filenames:
    #     print(df)
    dm = DetectorManager()
    dm.readMeta(meta_filenames[0])
    for filename in detector_filenames:
        dm.appendResults(str(filename))
    for detkey in dm.detectors:
        print(f"{detkey}  :  {len(dm.detectors[detkey].prima_results)}")
        dm.detectors[detkey].mergeResults()
        dm.detectors[detkey].dump_to_file(
            dm.detectors[detkey].addit_results[0],
            str(Path(results_dir).joinpath(detkey+'.det.txt'))
            )


    
