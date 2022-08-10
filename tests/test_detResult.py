import pytest
from anadet.detResult import *
import math
from pathlib import Path
from tests.config import BASE_DIR

def test_processHeader():
    header = ['#class tools::histo::h1d',\
    '#title Fluence distribution on DiagDetPV-3-Spec detector',\
    '#dimension 1',\
    '#axis edges 1e-12 1.06241e-12 1.12872e-12 1.19916e-12 1.274e-12 1.35351e-12 1.43798e-12 1.52773e-12 1.62307e-12 1.72437e-12 1.83199e-12',\
    '#annotation axis_x.title  [MeV]',\
    '#bin_number 12',\
    'entries,Sw,Sw2,Sxw0,Sx2w0']
    dr = DetResult()
    dr.processHeader(header)
    assert dr.title == "Fluence distribution on DiagDetPV-3-Spec detector"
    assert len(DetResult.BINS) == 1
    assert len(DetResult.BINS[dr.bin_index]) == 11
    assert math.isclose(DetResult.BINS[dr.bin_index][1], 1.06241e-12, rel_tol=1e-4)

    header = ['#class tools::histo::h1d',\
    '#title second testtitle',\
    '#dimension 1',\
    '#axis edges 1e-12 1.06241e-12 1.12872e-12 1.19916e-12 1.274e-12 1.35351e-12 1.43798e-12 1.52773e-12 1.62307e-12 1.72437e-12 1.83199e-12',\
    '#annotation axis_x.title  [MeV]',\
    '#bin_number 12',\
    'entries,Sw,Sw2,Sxw0,Sx2w0']
    dr2 = DetResult()
    dr2.processHeader(header)
    assert dr2.title == "second testtitle"
    assert len(DetResult.BINS) == 1
    assert len(DetResult.BINS[dr2.bin_index]) == 11
    assert math.isclose(DetResult.BINS[dr2.bin_index][1], 1.06241e-12, rel_tol=1e-4)

    header = ['#class tools::histo::h1d',\
    '#title third-testtitle',\
    '#dimension 1',\
    '#axis fixed 20 0 180',\
    '#annotation axis_x.title  [MeV]',\
    '#bin_number 22',\
    'entries,Sw,Sw2,Sxw0,Sx2w0']
    dr3 = DetResult()
    dr3.processHeader(header)
    assert dr3.title == "third-testtitle"
    assert len(DetResult.BINS) == 2
    assert len(DetResult.BINS[dr3.bin_index]) == 21
    assert math.isclose(DetResult.BINS[dr3.bin_index][1], 9, rel_tol=1e-4)

    #Header exceptions:
    header = [""]*7 # empty file case
    dr4 = DetResult()
    with pytest.raises(CSVHeaderError):
        dr4.processHeader(header)

    header = ['#class tools::histo::h2d',\
    '#title second testtitle',\
    '#dimension 1',\
    '#axis edges 1e-12 1.06241e-12 1.12872e-12 1.19916e-12 1.274e-12 1.35351e-12 1.43798e-12 1.52773e-12 1.62307e-12 1.72437e-12 1.83199e-12',\
    '#annotation axis_x.title  [MeV]',\
    '#bin_number 12',\
    'entries,Sw,Sw2,Sxw0,Sx2w0'] # vrong 1st string
    dr5 = DetResult()
    with pytest.raises(CSVHeaderError):
        dr5.processHeader(header)

    header = ['#class tools::histo::h1d',\
    '#title second testtitle',\
    '#dimension 1',\
    '#axis unknown 1.52773e-12 1.62307e-12 1.72437e-12 1.83199e-12',\
    '#annotation axis_x.title  [MeV]',\
    '#bin_number 12',\
    'entries,Sw,Sw2,Sxw0,Sx2w0'] # vrong 4th string
    dr6 = DetResult()
    with pytest.raises(CSVHeaderError):
        dr6.processHeader(header)

def test_readData():
    filename = str(BASE_DIR.joinpath('tests/test_resources/tests_1/1 MeV 10kk/results-master_h1_DiagDetPV-3-Spec.csv'))
    dr = DetResult()
    try:
        dr.readDataFromCSV(filename)
    except Exception as e:
        assert False, f"exception in test_readData: {e}"
    
    assert dr.title == "Fluence distribution on DiagDetPV-3-Spec detector"
    assert math.isclose(dr.overflow_bot, 871.143, rel_tol=1e-4)
    assert math.isclose(dr.overflow_top, 299.061, rel_tol=1e-4)
    assert dr.data_size == 10
    assert len(dr.y) == len(dr.y2) == 10
    assert len(DetResult.BINS[dr.bin_index]) == 11 # 10 data "y" + 1 for bottom edge => 11 edges
    assert math.isclose(dr.y[0], 615.654, rel_tol=1e-4)
    assert math.isclose(dr.y[2], 618.079, rel_tol=1e-4)
    assert math.isclose(dr.y[9], 233.417, rel_tol=1e-4)
    assert math.isclose(dr.y2[0], 43932.7, rel_tol=1e-4)
    assert math.isclose(dr.y2[5], 8475.79, rel_tol=1e-4)
    
def test_dataMerge():
    dr1 = DetResult()
    dr2 = DetResult()
    dr3 = DetResult()
    TEST_DIR = BASE_DIR.joinpath('tests/test_resources/filenames_and_grouping')
    filename1 = str( TEST_DIR.joinpath('1 keV 6kk/someName_h1_SpecDetDiag-2.csv') )
    filename2 = str( TEST_DIR.joinpath('1 keV 10kk/someName_h1_SpecDetDiag-2.csv') )
    filename3 = str( TEST_DIR.joinpath('1 keV 19kk/someName_h1_SpecDetDiag-2.csv') )
    dr1.readDataFromCSV(filename1)
    dr2.readDataFromCSV(filename2)
    dr3.readDataFromCSV(filename3)

    dr = DetResult()
    dr.appendData(dr1)
    dr.appendData(dr2)
    dr.appendData(dr3)

    assert math.isclose( dr.y[0], 615.654 + 9493.32 + 17176.3, abs_tol=1e-4 )
    assert math.isclose( dr.y[3], 576.182 + 11508.3 + 17059.4, abs_tol=1e-4 )
    assert math.isclose( dr.overflow_top, 299.061 + 16435.7 + 17625.1, abs_tol=1e-4 )
    assert dr.nhists == 35e+6
