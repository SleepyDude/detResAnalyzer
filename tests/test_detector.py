from anadet.detector import Detector, DetectorProps, SourceProps
from tests.config import BASE_DIR
from pathlib import Path

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