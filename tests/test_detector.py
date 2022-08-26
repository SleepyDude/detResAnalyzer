from anadet.detector import Detector, DetectorProps, SourceProps
from tests.config import BASE_DIR
from pathlib import Path
import math

def test_appendResult():
    sp = SourceProps(1, 'keV')
    dp = DetectorProps(sp)
    d = Detector(dp)
    dirname = BASE_DIR.joinpath('tests/test_resources/filenames_and_grouping')
    fname1 = '1 keV 6kk/someName_h1_SpecDetDiag-2.csv' # valid 
    fname2 = '1 keV 10kk/someName_h1_SpecDetDiag-2.csv' # valid
    fname3 = '1 keV 6kk/someName_h1_SpecDetDiag-1.csv' # not valid 
    d.appendResult(str(dirname.joinpath(fname1)))
    d.appendResult(str(dirname.joinpath(fname2)))
    d.appendResult(str(dirname.joinpath(fname3)))
    assert len(d.prima_results) == 2
    assert len(d.wrong_results) == 1
    assert Path(d.wrong_results[0]).match('1 keV 6kk/someName_h1_SpecDetDiag-1.csv')

def test_append_result_from_txt():
    dirname = BASE_DIR.joinpath('tests/test_resources/filenames_and_grouping')
    fname = 'merged/Phi_Diag-1_SRC[1.00 MeV].det.txt'
    fname = dirname.joinpath(fname)

    d = Detector()
    d.createFromFile(fname)
    assert len(d.prima_results) == 1
    assert len(d.wrong_results) == 0
    assert len(d.addit_results) == 0

    dp = d.detProps

    assert dp.num == 1
    assert dp.quantity == 'Phi'
    assert len(dp.tags) == 1
    assert dp.tags[0] == 'Diag'
    assert math.isclose(dp.geom_props.angle, 0.000508761, abs_tol=1e-14)
    assert math.isclose(dp.geom_props.distance, 1107.519752, abs_tol=1e-14)
    assert math.isclose(dp.src_props.energy, 1.0, abs_tol=1e-14)
    assert dp.src_props.energy_unit == 'MeV'
    assert d.createName(dp) == 'Phi_Diag-1_SRC[1.00 MeV]'
    
    det_res = d.prima_results[0]
    assert det_res.name == 'Phi_Diag-1_SRC[1.00 MeV]'
    bins = det_res.BINS[det_res.bin_index]
    assert len(bins) == 361
    assert math.isclose(bins[0], 0, abs_tol=1e-14)
    assert math.isclose(bins[11], 11.0, abs_tol=1e-14)
    assert det_res.stat.nhists == 5.5e+7
    assert math.isclose(det_res.overflow_bot, 3.0, abs_tol=1e-14)
    assert math.isclose(det_res.overflow_top, 5.0, abs_tol=1e-14)
    assert len(det_res.y) == len(det_res.y2) == 360
    assert math.isclose(det_res.y[0], 273, abs_tol=1e-14)
    assert math.isclose(det_res.y2[207], 11022.0, abs_tol=1e-14)
    assert len(det_res.origin_sequence) == 1
    assert len(det_res.origin_sequence[0].split()[0]) == 'READ:'
