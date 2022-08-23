from anadet.detRes import DetRes
from anadet.detectorManager import DetectorManager
from anadet.filesManager import FilesManager
from pprint import pprint as pp
from tests.config import BASE_DIR
from pytest import fixture

@fixture
def fm():
    test_directory = str(BASE_DIR.joinpath('tests/test_resources/filenames_and_grouping'))
    fm = FilesManager()
    fm.readDirectory(test_directory)
    return fm

def test_grouping(fm):
    detector_filenames = fm.getDetFiles()
    dm = DetectorManager()
    for filename in detector_filenames:
        dm.appendResults(str(filename))
    assert 'Spec_Diag-1_SRC[1.00 keV]' in dm.detectors
    assert len(dm.detectors['Spec_Diag-1_SRC[1.00 keV]'].wrong_results) == 3
    assert len(dm.detectors['Spec_Diag-1_SRC[1.00 keV]'].prima_results) == 0
    assert len(dm.detectors['Phi_Diag-1_SRC[1.00 keV]'].prima_results) == 0
    assert len(dm.detectors['Spec_Diag-5_SRC[0.50 MeV]'].prima_results) == 0
    
    assert len(dm.detectors['Spec_Diag-2_SRC[1.00 keV]'].prima_results) == 3
    assert type(dm.detectors['Spec_Diag-2_SRC[1.00 keV]'].prima_results[0]) == DetRes

def test_read_meta(fm):
    meta_filenames = fm.getMetaFiles()
    dm = DetectorManager()
    assert len(dm.meta_info) == 0
    dm.readMeta(meta_filenames[0])
    assert len(dm.meta_info) == 4
    assert 'Vert' in dm.meta_info
    assert 'XWall' in dm.meta_info
    assert 'YWall' in dm.meta_info
    assert 'Diag' in dm.meta_info
    assert len(dm.meta_info['Vert']) == 8
    assert len(dm.meta_info['XWall']) == 10
    assert len(dm.meta_info['YWall']) == 10
    assert len(dm.meta_info['Diag']) == 10

    assert '1' in dm.meta_info['Vert']
    assert '8' in dm.meta_info['Vert']
    assert 'distance' in dm.meta_info['Vert']['8']



    