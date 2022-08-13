from anadet.detRes import DetRes
from anadet.detectorManager import DetectorManager
from anadet.filesManager import FilesManager
from pprint import pprint as pp
from tests.config import BASE_DIR

# TODO - make this test depends on FileManager tests
def test_grouping():
    test_directory = str(BASE_DIR.joinpath('tests/test_resources/filenames_and_grouping'))
    fm = FilesManager()
    fm.readDirectory(test_directory)
    detector_filenames = fm.getDetFiles()
    dm = DetectorManager()
    for filename in detector_filenames:
        dm.appendResults(str(filename))
    assert 'Spec|Diag-1|SRC:[1.00 keV]' in dm.detectors
    assert len(dm.detectors['Spec|Diag-1|SRC:[1.00 keV]'].wrong_results) == 3
    assert len(dm.detectors['Spec|Diag-1|SRC:[1.00 keV]'].prima_results) == 0
    assert len(dm.detectors['Phi|Diag-1|SRC:[1.00 keV]'].prima_results) == 0
    assert len(dm.detectors['Spec|Diag-5|SRC:[0.50 MeV]'].prima_results) == 0
    
    assert len(dm.detectors['Spec|Diag-2|SRC:[1.00 keV]'].prima_results) == 3
    assert type(dm.detectors['Spec|Diag-2|SRC:[1.00 keV]'].prima_results[0]) == DetRes