from ..anadet.detRes import DetRes
from ..anadet.detectorManager import DetectorManager
from ..anadet.filesManager import FilesManager
from .config import BASE_DIR
import pytest
import math

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

def test_grouping(fm):
    detector_filenames = fm.getDetFiles()
    dm = DetectorManager()
    for filename in detector_filenames:
        dm.appendResults(str(filename))
    assert 'Spec_Diag_1_SRC[1.00 keV]' in dm.detectors
    assert len(dm.detectors['Spec_Diag_1_SRC[1.00 keV]'].wrong_results) == 3
    assert len(dm.detectors['Spec_Diag_1_SRC[1.00 keV]'].prima_results) == 0
    assert len(dm.detectors['Phi_Diag_1_SRC[1.00 keV]'].prima_results) == 0
    assert len(dm.detectors['Spec_Diag_5_SRC[0.50 MeV]'].prima_results) == 0
    
    assert len(dm.detectors['Spec_Diag_2_SRC[1.00 keV]'].prima_results) == 3
    assert type(dm.detectors['Spec_Diag_2_SRC[1.00 keV]'].prima_results[0]) == DetRes

def test_read_meta(fm):
    meta_filenames = fm.getMetaFiles()
    dm = DetectorManager()
    assert len(dm.meta_categories) == 0
    assert len(dm.meta_data) == 0
    dm.readMeta(meta_filenames[0])
    assert len(dm.meta_categories) == 2
    assert len(dm.meta_data) == 38
    assert type(dm.meta_categories) == list
    assert type(dm.meta_data) == dict
    assert 'Vert-1' in dm.meta_data
    assert 'Vert-8' in dm.meta_data
    assert 'XWall-1' in dm.meta_data
    assert 'XWall-10' in dm.meta_data
    assert  'distance' in dm.meta_data['Vert-1']
    assert  'angle' in dm.meta_data['Diag-5']

def test_append_result_with_meta(fm):
    detector_filenames = fm.getDetFiles()
    meta_filenames = fm.getMetaFiles()
    dm = DetectorManager()
    dm.readMeta(meta_filenames[0]) # important part in this test
    for filename in detector_filenames:
        dm.appendResults(str(filename))

    assert math.isclose(dm.detectors['Spec_Diag_1_SRC[1.00 keV]'].detProps.geom_props.angle, 0.000508761, abs_tol=1e-14)
    assert math.isclose(dm.detectors['Spec_Diag_1_SRC[1.00 keV]'].detProps.geom_props.distance, 1107.519752, abs_tol=1e-14)
    assert math.isclose(dm.detectors['Phi_Diag_1_SRC[1.00 keV]'].detProps.geom_props.angle, 0.000508761, abs_tol=1e-14)
    assert math.isclose(dm.detectors['Phi_Diag_1_SRC[1.00 keV]'].detProps.geom_props.distance, 1107.519752, abs_tol=1e-14)

def test_filter_energy(dm: DetectorManager):
    detectors = dm.prep_dets_for_filtering(dm.detectors)

    res_detectors = dm.filterEnergies(detectors, [(0.1, 'MeV')])
    assert 'Spec_Diag_1' in res_detectors
    assert 'Spec_Diag_2' in res_detectors
    assert 'Spec_Diag_3' in res_detectors
    assert 'Spec_Diag_4' in res_detectors
    assert 'Spec_Diag_5' in res_detectors
    assert 'Spec_Diag_6' in res_detectors
    assert len(res_detectors) == 6

    res_detectors2 = dm.filterEnergies(detectors, [(1, 'keV')])
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

    res_detectors3 = dm.filterEnergies(detectors, [(10, 'keV')])
    assert len(res_detectors3) == 0

def test_filter_quantity(dm: DetectorManager):
    detectors = dm.prep_dets_for_filtering(dm.detectors)

    res_detectors = dm.filterQuantity(detectors, 'Phi')
    assert 'Diag_1_SRC[0.50 MeV]' in res_detectors
    assert 'Diag_1_SRC[1.00 keV]' in res_detectors
    assert 'Diag_2_SRC[1.00 keV]' in res_detectors
    assert 'Diag_3_SRC[1.00 keV]' in res_detectors
    assert 'Diag_1_SRC[1.00 MeV]' in res_detectors
    assert len(res_detectors) == 5

    res_detectors2 = dm.filterQuantity(detectors, 'Spec')
    assert 'Diag_1_SRC[0.10 MeV]' in res_detectors2
    assert 'Diag_4_SRC[0.10 MeV]' in res_detectors2
    assert 'Diag_1_SRC[0.50 MeV]' in res_detectors2
    assert 'Diag_4_SRC[0.50 MeV]' in res_detectors2
    assert 'Diag_6_SRC[0.50 MeV]' in res_detectors2
    assert 'Diag_3_SRC[1.00 keV]' in res_detectors2
    assert 'Vert_2_SRC[1.00 keV]' in res_detectors2
    assert len(res_detectors2) == 20

    res_detectors3 = dm.filterQuantity(detectors, 'Theta')
    assert len(res_detectors3) == 0

def test_filter_tag(dm: DetectorManager):
    detectors = dm.prep_dets_for_filtering(dm.detectors)

    res_detectors = dm.filterTag(detectors, 'Vert')
    assert 'Spec_1_SRC[1.00 keV]' in res_detectors
    assert 'Spec_2_SRC[1.00 keV]' in res_detectors
    assert len(res_detectors) == 2

    res_detectors2 = dm.filterTag(detectors, 'XWall')
    assert len(res_detectors2) == 0

    res_detectors3 = dm.filterTag(detectors, 'Diag')
    assert 'Spec_1_SRC[0.10 MeV]' in res_detectors3
    assert 'Spec_3_SRC[0.10 MeV]' in res_detectors3
    assert 'Spec_3_SRC[0.50 MeV]' in res_detectors3
    assert 'Phi_2_SRC[1.00 keV]' in res_detectors3
    assert 'Phi_1_SRC[0.50 MeV]' in res_detectors3
    assert 'Phi_1_SRC[1.00 MeV]' in res_detectors3
    assert len(res_detectors3) == 23

def test_filter_sequence(dm: DetectorManager):
    detectors = dm.prep_dets_for_filtering(dm.detectors)
    res = dm.filterQuantity(detectors, 'Spec')
    res = dm.filterTag(res, 'Diag')
    res = dm.filterEnergies(res, [(1, 'keV')])
    assert len(res) == 6
    assert '1' in res
    assert '2' in res
    assert '6' in res

if __name__ == "__main__":
    pytest.main(["tests/test_detectorManager.py", "-s"])