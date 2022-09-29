from ..anadet.detectorManager import DetectorManager
from ..anadet.filesManager import FilesManager
from ..anadet.detectorUtils import prep_dets_for_filtering, filterEnergies, filterNums, filterQuantity, filterTag
from .config import BASE_DIR
import pytest

@pytest.fixture
def fm():
    test_directory = str(BASE_DIR.joinpath('tests/test_resources/filenames_and_grouping'))
    fm = FilesManager()
    fm.readDirectory(test_directory)
    return fm

@pytest.fixture
def dm(fm) -> DetectorManager:
    detector_filenames = fm.getDetFiles()
    meta_filenames = fm.getMetaFiles()
    dm = DetectorManager()
    dm.readMeta(meta_filenames[0])
    for filename in detector_filenames:
        dm.appendResults(str(filename))
    return dm

def test_filter_energy(dm: DetectorManager):
    detectors = prep_dets_for_filtering(dm.detectors)

    res_detectors = filterEnergies(detectors, [(0.1, 'MeV')])
    assert 'Spec_Diag_1' in res_detectors
    assert 'Spec_Diag_2' in res_detectors
    assert 'Spec_Diag_3' in res_detectors
    assert 'Spec_Diag_4' in res_detectors
    assert 'Spec_Diag_5' in res_detectors
    assert 'Spec_Diag_6' in res_detectors
    assert len(res_detectors) == 6

    res_detectors2 = filterEnergies(detectors, [(1, 'keV')])
    assert 'Phi_Diag_1' in res_detectors2
    assert 'Phi_Diag_2' in res_detectors2
    assert 'Phi_Diag_3' in res_detectors2
    assert 'Spec_Diag_1' in res_detectors2
    assert 'Spec_Diag_2' in res_detectors2
    assert 'Spec_Diag_3' in res_detectors2
    assert 'Spec_Diag_4' in res_detectors2
    assert 'Spec_Diag_5' in res_detectors2
    assert 'Spec_Diag_6' in res_detectors2
    assert 'Spec_Vert_1' in res_detectors2
    assert 'Spec_Vert_2' in res_detectors2
    assert len(res_detectors2) == 11

    res_detectors3 = filterEnergies(detectors, [(10, 'keV')])
    assert len(res_detectors3) == 0

def test_filter_quantity(dm: DetectorManager):
    detectors = prep_dets_for_filtering(dm.detectors)

    res_detectors = filterQuantity(detectors, 'Phi')
    assert 'Diag_1_SRC[0.50 MeV]' in res_detectors
    assert 'Diag_1_SRC[1.00 keV]' in res_detectors
    assert 'Diag_2_SRC[1.00 keV]' in res_detectors
    assert 'Diag_3_SRC[1.00 keV]' in res_detectors
    assert 'Diag_1_SRC[1.00 MeV]' in res_detectors
    assert len(res_detectors) == 5

    res_detectors2 = filterQuantity(detectors, 'Spec')
    assert 'Diag_1_SRC[0.10 MeV]' in res_detectors2
    assert 'Diag_4_SRC[0.10 MeV]' in res_detectors2
    assert 'Diag_1_SRC[0.50 MeV]' in res_detectors2
    assert 'Diag_4_SRC[0.50 MeV]' in res_detectors2
    assert 'Diag_6_SRC[0.50 MeV]' in res_detectors2
    assert 'Diag_3_SRC[1.00 keV]' in res_detectors2
    assert 'Vert_2_SRC[1.00 keV]' in res_detectors2
    assert len(res_detectors2) == 20

    res_detectors3 = filterQuantity(detectors, 'Theta')
    assert len(res_detectors3) == 0

def test_filter_tag(dm: DetectorManager):
    detectors = prep_dets_for_filtering(dm.detectors)

    res_detectors = filterTag(detectors, 'Vert')
    assert 'Spec_1_SRC[1.00 keV]' in res_detectors
    assert 'Spec_2_SRC[1.00 keV]' in res_detectors
    assert len(res_detectors) == 2

    res_detectors2 = filterTag(detectors, 'XWall')
    assert len(res_detectors2) == 0

    res_detectors3 = filterTag(detectors, 'Diag')
    assert 'Spec_1_SRC[0.10 MeV]' in res_detectors3
    assert 'Spec_3_SRC[0.10 MeV]' in res_detectors3
    assert 'Spec_3_SRC[0.50 MeV]' in res_detectors3
    assert 'Phi_2_SRC[1.00 keV]' in res_detectors3
    assert 'Phi_1_SRC[0.50 MeV]' in res_detectors3
    assert 'Phi_1_SRC[1.00 MeV]' in res_detectors3
    assert len(res_detectors3) == 23

def test_filter_sequence(dm: DetectorManager):
    detectors = prep_dets_for_filtering(dm.detectors)
    res = filterQuantity(detectors, 'Spec')
    res = filterTag(res, 'Diag')
    res = filterEnergies(res, [(1, 'keV')])
    assert len(res) == 6
    assert '1' in res
    assert '2' in res
    assert '6' in res