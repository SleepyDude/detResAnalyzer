from ..anadet.detectorManager import DetectorManager
from ..anadet.filesManager import FilesManager
from ..anadet.detectorUtils import prep_dets_for_filtering, filterEnergies, filterNums, filterQuantity, filterTag
from ..anadet.detectorUtils import order_dets
from ..anadet.detector import Detector, DetectorProps, SourceProps
from .config import BASE_DIR
import pytest
from typing import Tuple, Dict

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

@pytest.fixture
def detectors() -> Dict[str, Tuple[set, Detector]]:
    '''
    Creating the list of detectors for ordering testing
    Detectors:
        1. Spec  Vert  5 1 keV
        2. Phi   Diag  2 0.1 eV
        3. Theta Vert  1 1 eV
        4. Phi   Diag  1 4 MeV
        5. Theta XWall 4 2 MeV
        6. Theta YWall 2 1 keV
        7. Spec  XWall 2 1 keV
        8. Spec  XWall 3 3 keV
        9. Phi   YWall 6 0.4 eV
    '''
    res = dict()
    data = [
        ('Spec',  'Vert',  '5', 1, 'keV'),
        ('Phi',   'Diag',  '2', 0.1, 'eV'),
        ('Theta', 'Vert',  '1', 1, 'eV'),
        ('Phi',   'Diag',  '1', 4, 'MeV'),
        ('Theta', 'XWall', '4', 2, 'MeV'),
        ('Theta', 'YWall', '2', 1, 'keV'),
        ('Spec',  'XWall', '2', 1, 'keV'),
        ('Spec',  'XWall', '3', 3, 'keV'),
        ('Phi',   'YWall', '6', 0.4, 'eV'),
    ]
    for item in data:
        src_props = SourceProps(item[3], item[4])
        det_props = DetectorProps(src_props, item[0], item[2])
        det_props.setTag(item[1])
        d = Detector(det_props)
        res[d.detProps.getKeyname] = (set(), d)
    return res


@pytest.fixture
def tag_num_dets() -> Dict[str, Tuple[set, Detector]]:
    '''
    Creating the list of detectors for ordering testing
    Detectors:
        0. Spec Vert  5 1 keV
        1. Spec Diag  2 0.1 eV
        2. Spec Vert  1 1 keV
        3. Spec Diag  1 4 MeV
        4. Spec XWall 5 1 MeV
        5. Spec YWall 2 1 keV
        6. Spec XWall 2 1 MeV
        7. Spec XWall 3 1 MeV
        9. Spec YWall 2 0.4 eV
       10. Spec Vert  3 1 keV
       11. Spec Diag  6 4 MeV
       12. Spec Vert  2 0.4 eV
       13. Spec Diag  4 0.1 eV
       14. Spec YWall 2 10 keV
       15. Spec YWall 2 1 MeV
       16. Spec XWall 6 1 MeV
       17. Spec XWall 1 1 MeV
    '''
    res = dict()
    data = [
        ("Spec", "Vert",  "5", 1, "keV"),
        ("Spec", "Diag",  "2", 0.1, "eV"),
        ("Spec", "Vert",  "1", 1, "keV"),
        ("Spec", "Diag",  "1", 4, "MeV"),
        ("Spec", "XWall", "5", 1, "MeV"),
        ("Spec", "YWall", "2", 1, "keV"),
        ("Spec", "XWall", "2", 1, "MeV"),
        ("Spec", "XWall", "3", 1, "MeV"),
        ("Spec", "YWall", "2", 0.4, "eV"),
        ("Spec", "Vert",  "3", 1, "keV"),
        ("Spec", "Diag",  "6", 4, "MeV"),
        ("Spec", "Vert",  "2", 0.4, "eV"),
        ("Spec", "Diag",  "4", 0.1, "eV"),
        ("Spec", "YWall", "2", 10, "keV"),
        ("Spec", "YWall", "2", 1, "MeV"),
        ("Spec", "XWall", "6", 1, "MeV"),
        ("Spec", "XWall", "1", 1, "MeV"),
    ]
    for item in data:
        src_props = SourceProps(item[3], item[4])
        det_props = DetectorProps(src_props, item[0], item[2])
        det_props.setTag(item[1])
        d = Detector(det_props)
        res[d.detProps.getKeyname] = (set(), d)
    return res

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

def test_ordering(detectors: Dict[str, Tuple[set, Detector]]):
    prim_dets = list()
    for _, value in detectors.items():
        prim_dets.append(value[1])

    dets = order_dets(detectors)
    # let's put them into list for convenience
    '''
    Detectors:
                                  Q   T   E   N  RES
        0. Spec  Vert  5 1 keV  | 1 | 1 | 3 | 5 | 1135 | 3     
        1. Phi   Diag  2 0.1 eV | 0 | 0 | 0 | 2 | 2    | 0 
        2. Theta Vert  1 1 eV   | 2 | 1 | 2 | 1 | 2121 | 6    
        3. Phi   Diag  1 4 MeV  | 0 | 0 | 6 | 1 | 61   | 1 
        4. Theta XWall 4 2 MeV  | 2 | 2 | 5 | 4 | 2254 | 7    
        5. Theta YWall 2 1 keV  | 2 | 3 | 3 | 2 | 2332 | 8    
        6. Spec  XWall 2 1 keV  | 1 | 2 | 3 | 2 | 1232 | 4   
        7. Spec  XWall 3 3 keV  | 1 | 2 | 4 | 3 | 1243 | 5   
        8. Phi   YWall 6 0.4 eV | 0 | 3 | 1 | 6 | 316  | 2   
    '''
    sort_dets = list()
    for _, value in dets.items():
        sort_dets.append(value[1])
    assert sort_dets[0] == prim_dets[1]
    assert sort_dets[1] == prim_dets[3]
    assert sort_dets[2] == prim_dets[8]
    assert sort_dets[3] == prim_dets[0]
    assert sort_dets[4] == prim_dets[6]
    assert sort_dets[5] == prim_dets[7]
    assert sort_dets[6] == prim_dets[2]
    assert sort_dets[7] == prim_dets[4]
    assert sort_dets[8] == prim_dets[5]
