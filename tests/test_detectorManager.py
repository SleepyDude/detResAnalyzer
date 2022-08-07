from anadet.detectorManager import DetectorManager
from anadet.filesManager import FilesManager
from pathlib import Path
import pytest
from pprint import pprint as pp

BASE_DIR = Path(__file__).resolve().parent.parent

# TODO - make this test depends on FileManager tests
def test_grouping():
    test_directory = str(BASE_DIR.joinpath('tests/test_resources/filenames_and_grouping'))
    fm = FilesManager()
    fm.readDirectory(test_directory)
    detector_filenames = fm.getDetFiles()
    dm = DetectorManager()
    for file in detector_filenames:
        dm.appendResults(file)
    assert 'Spec|Diag-1|SRC:[1.00 keV]' in dm.detectors
    assert len(dm.detectors['Spec|Diag-1|SRC:[1.00 keV]'].results) == 3
    assert len(dm.detectors['Phi|Diag-1|SRC:[1.00 keV]'].results) == 2
    assert len(dm.detectors['Spec|Diag-5|SRC:[0.50 MeV]'].results) == 1