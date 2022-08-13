import pytest
from anadet.detRes import DetRes
import math
from pathlib import Path
from tests.config import BASE_DIR

def test_processCSVHeader():
    header = ['#class tools::histo::h1d',\
    '#title Fluence distribution on DiagDetPV-3-Spec detector',\
    '#dimension 1',\
    '#axis edges 1e-12 1.06241e-12 1.12872e-12 1.19916e-12 1.274e-12 1.35351e-12 1.43798e-12 1.52773e-12 1.62307e-12 1.72437e-12 1.83199e-12',\
    '#annotation axis_x.title  [MeV]',\
    '#bin_number 12',\
    'entries,Sw,Sw2,Sxw0,Sx2w0']
    dr = DetRes()
    dr.processCSVHeader(header)
    assert dr.data_size == 10
    assert len(DetRes.BINS) == 1
    assert len(DetRes.BINS[dr.bin_index]) == 11
    assert math.isclose(DetRes.BINS[dr.bin_index][1], 1.06241e-12, rel_tol=1e-4)

    header = ['#class tools::histo::h1d',\
    '#title second testtitle',\
    '#dimension 1',\
    '#axis edges 1e-12 1.06241e-12 1.12872e-12 1.19916e-12 1.274e-12 1.35351e-12 1.43798e-12 1.52773e-12 1.62307e-12 1.72437e-12 1.83199e-12',\
    '#annotation axis_x.title  [MeV]',\
    '#bin_number 12',\
    'entries,Sw,Sw2,Sxw0,Sx2w0']
    dr2 = DetRes()
    dr2.processCSVHeader(header)
    assert len(DetRes.BINS) == 1
    assert len(DetRes.BINS[dr2.bin_index]) == 11
    assert math.isclose(DetRes.BINS[dr2.bin_index][1], 1.06241e-12, rel_tol=1e-4)

    header = ['#class tools::histo::h1d',\
    '#title third-testtitle',\
    '#dimension 1',\
    '#axis fixed 20 0 180',\
    '#annotation axis_x.title  [MeV]',\
    '#bin_number 22',\
    'entries,Sw,Sw2,Sxw0,Sx2w0']
    dr3 = DetRes()
    dr3.processCSVHeader(header)
    assert len(DetRes.BINS) == 2
    assert len(DetRes.BINS[dr3.bin_index]) == 21
    assert math.isclose(DetRes.BINS[dr3.bin_index][1], 9, rel_tol=1e-4)

    #Header exceptions:
    header = [""]*7 # empty file case
    dr4 = DetRes()
    with pytest.raises(DetRes.CSVHeaderError):
        dr4.processCSVHeader(header)

    header = ['#class tools::histo::h2d',\
    '#title second testtitle',\
    '#dimension 1',\
    '#axis edges 1e-12 1.06241e-12 1.12872e-12 1.19916e-12 1.274e-12 1.35351e-12 1.43798e-12 1.52773e-12 1.62307e-12 1.72437e-12 1.83199e-12',\
    '#annotation axis_x.title  [MeV]',\
    '#bin_number 12',\
    'entries,Sw,Sw2,Sxw0,Sx2w0'] # vrong 1st string
    dr5 = DetRes()
    with pytest.raises(DetRes.CSVHeaderError):
        dr5.processCSVHeader(header)

    header = ['#class tools::histo::h1d',\
    '#title second testtitle',\
    '#dimension 1',\
    '#axis unknown 1.52773e-12 1.62307e-12 1.72437e-12 1.83199e-12',\
    '#annotation axis_x.title  [MeV]',\
    '#bin_number 12',\
    'entries,Sw,Sw2,Sxw0,Sx2w0'] # vrong 4th string
    dr6 = DetRes()
    with pytest.raises(DetRes.CSVHeaderError):
        dr6.processCSVHeader(header)

def test_readData():
    filename = str(BASE_DIR.joinpath('tests/test_resources/tests_1/1 MeV 10kk/results-master_h1_DiagDetPV-3-Spec.csv'))
    dr = DetRes()
    try:
        dr.readDataFromCSV(filename)
    except Exception as e:
        assert False, f"exception in test_readData: {e}"
    
    assert math.isclose(dr.overflow_bot, 871.143, rel_tol=1e-4)
    assert math.isclose(dr.overflow_top, 299.061, rel_tol=1e-4)
    assert len(dr.y) == len(dr.y2) == 10
    assert len(DetRes.BINS[dr.bin_index]) == 11 # 10 data "y" + 1 for bottom edge => 11 edges
    assert math.isclose(dr.y[0], 615.654, rel_tol=1e-4)
    assert math.isclose(dr.y[2], 618.079, rel_tol=1e-4)
    assert math.isclose(dr.y[9], 233.417, rel_tol=1e-4)
    assert math.isclose(dr.y2[0], 43932.7, rel_tol=1e-4)
    assert math.isclose(dr.y2[5], 8475.79, rel_tol=1e-4)
    
def test_dataAppend():
    dr1 = DetRes()
    dr2 = DetRes()
    dr3 = DetRes()
    TEST_DIR = BASE_DIR.joinpath('tests/test_resources/filenames_and_grouping')
    filename1 = str( TEST_DIR.joinpath('1 keV 6kk/someName_h1_SpecDetDiag-2.csv') )
    filename2 = str( TEST_DIR.joinpath('1 keV 10kk/someName_h1_SpecDetDiag-2.csv') )
    filename3 = str( TEST_DIR.joinpath('1 keV 19kk/someName_h1_SpecDetDiag-2.csv') )
    dr1.readDataFromCSV(filename1)
    dr2.readDataFromCSV(filename2)
    dr3.readDataFromCSV(filename3)

    dr = DetRes()
    dr.appendData(dr1)
    dr.appendData(dr2)
    dr.appendData(dr3)

    assert math.isclose( dr.y[0], 615.654 + 9493.32 + 17176.3, abs_tol=1e-4 )
    assert math.isclose( dr.y[3], 576.182 + 11508.3 + 17059.4, abs_tol=1e-4 )
    assert math.isclose( dr.overflow_top, 299.061 + 16435.7 + 17625.1, abs_tol=1e-4 )
    assert dr.nhists == 35e+6

def test_statisticsCalculate():
    dr = DetRes()
    TEST_DIR = BASE_DIR.joinpath('tests/test_resources/filenames_and_grouping')
    fname = str( TEST_DIR.joinpath('1 keV 6kk/someName_h1_SpecDetDiag-2.csv') )
    dr.readDataFromCSV(fname)
    dr.calculateStatistics()
    assert len(dr.M) == len(dr.D) == len(dr.sigma) == len(dr.y) == len(dr.y2) == 10
    assert math.isclose(dr.M[0], 1.02609e-4, rel_tol=1e-4)
    assert math.isclose(dr.M[9], 3.890283333e-5, rel_tol=1e-4)
    assert math.isclose(dr.D[0], 7.32211e-3, rel_tol=1e-4)
    assert math.isclose(dr.D[9], 2.80447e-3, rel_tol=1e-4)
    assert math.isclose(dr.sigma[0], 3.49335e-5, rel_tol=1e-4)
    assert math.isclose(dr.sigma[9], 2.16197e-5, rel_tol=1e-4)
    assert math.isclose(dr.delta[0], 3.40453e-1, rel_tol=1e-4)
    assert math.isclose(dr.delta[9], 5.55736e-1, rel_tol=1e-4)
    