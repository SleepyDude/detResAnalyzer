import pytest
import math
# from tests.config import BASE_DIR
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

from anadet.detRes import DetRes


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
    assert len(dr.origin_sequence) == 3
    first_words = [i.split()[0] for i in dr.origin_sequence]
    first_words_right = ['APPEND:', 'APPEND:', 'APPEND:']
    assert ''.join(first_words) == ''.join(first_words_right)

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
    
def test_createChild_1():
    dr = DetRes()
    TEST_DIR = BASE_DIR.joinpath('tests/test_resources/filenames_and_grouping')
    fname = str(TEST_DIR.joinpath("0.5 MeV 8kk/someName_h1_DetDiagPhi-1.csv"))
    dr.readDataFromCSV(fname)
    assert len(dr.BINS[dr.bin_index]) == 21
    assert math.isclose(dr.BINS[dr.bin_index][3], 1.5, rel_tol=1e-4)
    assert math.isclose(dr.y[4], 30, rel_tol=1e-4)
    assert math.isclose(dr.y2[4], 50, rel_tol=1e-4)

    # trivial case
    bins1 = [float(i) for i in range(11)]
    drChild1 = dr.createChild(bins1)
    assert len(drChild1.BINS[drChild1.bin_index]) == 11
    assert math.isclose(drChild1.y[1], 0, rel_tol=1e-4)
    assert math.isclose(drChild1.y[2], 30, rel_tol=1e-4)
    assert math.isclose(drChild1.y[3], 0, rel_tol=1e-4)

    assert math.isclose(drChild1.y2[1], 0, rel_tol=1e-4)
    assert math.isclose(drChild1.y2[2], 50, rel_tol=1e-4)
    assert math.isclose(drChild1.y2[3], 0, rel_tol=1e-4)

    # more complex case
    bins2 = [float(i)/4.0 for i in range(41)]
    drChild2 = dr.createChild(bins2)
    assert math.isclose(drChild2.y[7], 0, rel_tol=1e-4)
    assert math.isclose(drChild2.y[8], 15, rel_tol=1e-4)
    assert math.isclose(drChild2.y[9], 15, rel_tol=1e-4)
    assert math.isclose(drChild2.y[10], 0, rel_tol=1e-4)

    assert math.isclose(drChild2.y2[7], 0, rel_tol=1e-4)
    assert math.isclose(drChild2.y2[8], 25, rel_tol=1e-4)
    assert math.isclose(drChild2.y2[9], 25, rel_tol=1e-4)
    assert math.isclose(drChild2.y2[10], 0, rel_tol=1e-4)

    # irregular bin case
    #    yi          0    1    2    3    4    5    6  7
    #    xi     0    1    2    3    4    5    6    7  8
    bins3 = [-3.0, 0.3, 0.9, 1.3, 1.9, 2.1, 2.3, 3.3, 8]
    drChild3 = dr.createChild(bins3)
    assert math.isclose(drChild3.y[3], 0, rel_tol=1e-4)
    assert math.isclose(drChild3.y[4], 6, rel_tol=1e-4)
    assert math.isclose(drChild3.y[5], 12, rel_tol=1e-4)
    assert math.isclose(drChild3.y[6], 12, rel_tol=1e-4)
    assert math.isclose(drChild3.y[7], 0, rel_tol=1e-4)

    assert math.isclose(drChild3.y2[3], 0, rel_tol=1e-4)
    assert math.isclose(drChild3.y2[4], 10, rel_tol=1e-4)
    assert math.isclose(drChild3.y2[5], 20, rel_tol=1e-4)
    assert math.isclose(drChild3.y2[6], 20, rel_tol=1e-4)
    assert math.isclose(drChild3.y2[7], 0, rel_tol=1e-4)

def test_createChild_2():
    dr = DetRes()
    TEST_DIR = BASE_DIR.joinpath('tests/test_resources/filenames_and_grouping')
    fname = str(TEST_DIR.joinpath("0.5 MeV 5kk/someName_h1_SpecDetDiag-4.csv"))
    dr.readDataFromCSV(fname)
    assert len(dr.BINS[dr.bin_index]) == 11
    assert math.isclose(dr.BINS[dr.bin_index][3], 3, rel_tol=1e-4)
    assert math.isclose(dr.y[3], 16, rel_tol=1e-4)
    assert math.isclose(dr.y2[3], 15, rel_tol=1e-4)

    # trivial case 1
    bins1 = [float(i)*2 for i in range(6)]
    drChild1 = dr.createChild(bins1)
    assert len(drChild1.BINS[drChild1.bin_index]) == 6
    assert math.isclose(drChild1.y[0], 0, rel_tol=1e-4)
    assert math.isclose(drChild1.y[1], 16, rel_tol=1e-4)
    assert math.isclose(drChild1.y[2], 50, rel_tol=1e-4)
    assert math.isclose(drChild1.y[3], 5, rel_tol=1e-4)
    assert math.isclose(drChild1.y[4], 18, rel_tol=1e-4)

    assert math.isclose(drChild1.y2[0], 0, rel_tol=1e-4)
    assert math.isclose(drChild1.y2[1], 15, rel_tol=1e-4)
    assert math.isclose(drChild1.y2[2], 60, rel_tol=1e-4)
    assert math.isclose(drChild1.y2[3], 60, rel_tol=1e-4)
    assert math.isclose(drChild1.y2[4], 16, rel_tol=1e-4)

    assert math.isclose(drChild1.overflow_bot, 0, rel_tol=1e-4)
    assert math.isclose(drChild1.overflow_top, 3, rel_tol=1e-4)

    # trivial case 2
    bins2 = [float(i)*2 for i in range(4)]
    drChild2 = dr.createChild(bins2)
    assert len(drChild2.BINS[drChild2.bin_index]) == 4
    assert len(drChild2.y) == 3
    assert math.isclose(drChild2.y[0], 0, rel_tol=1e-4)
    assert math.isclose(drChild2.y[1], 16, rel_tol=1e-4)
    assert math.isclose(drChild2.y[2], 50, rel_tol=1e-4)

    assert math.isclose(drChild2.y2[0], 0, rel_tol=1e-4)
    assert math.isclose(drChild2.y2[1], 15, rel_tol=1e-4)
    assert math.isclose(drChild2.y2[2], 60, rel_tol=1e-4)

    assert math.isclose(drChild2.overflow_bot, 0, rel_tol=1e-4)
    assert math.isclose(drChild2.overflow_top, 26, rel_tol=1e-4)

    # irregular bin case
    #    yi          0    1    2    3    4    5    6    7    8    9   10   11   12   13 14   15
    #    xi     0    1    2    3    4    5    6    7    8    9   10   11   12   13   14 15   16
    bins3 = [-3.0, 0.3, 0.9, 1.3, 1.9, 2.1, 2.3, 3.3, 3.9, 4.4, 4.5, 4.8, 5.2, 6.9, 7.5, 8, 9.6]
    # test bins  0    1    2    3    4    5    6    7    8    9   10
    # test y          0    0    0   16   30   20    5    0    0   18   
    # test y2         0    0    0   15   50   10   60    0    0   16
    drChild3 = dr.createChild(bins3)
    assert math.isclose(drChild3.y[5], 0, rel_tol=1e-4)
    assert math.isclose(drChild3.y[6], 4.8, rel_tol=1e-4)
    assert math.isclose(drChild3.y[7], 9.6, rel_tol=1e-4)
    assert math.isclose(drChild3.y[8], 1.6+12, rel_tol=1e-4)
    assert math.isclose(drChild3.y[9], 3, rel_tol=1e-4)
    assert math.isclose(drChild3.y[10], 9, rel_tol=1e-4)
    assert math.isclose(drChild3.y[11], 6+4, rel_tol=1e-4)
    assert math.isclose(drChild3.y[12], 16+4.5, rel_tol=1e-4)
    assert math.isclose(drChild3.y[13], 0.5, rel_tol=1e-4)
    assert math.isclose(drChild3.y[14], 0.0, rel_tol=1e-4)
    assert math.isclose(drChild3.y[15], 10.8, rel_tol=1e-4)

    assert math.isclose(drChild3.overflow_top, 10.2, rel_tol=1e-4)

    assert math.isclose(drChild3.y2[5], 0, rel_tol=1e-4)
    assert math.isclose(drChild3.y2[6], 4.5, rel_tol=1e-4) # 0.3 * 15
    assert math.isclose(drChild3.y2[7], 9.0, rel_tol=1e-4) # 0.6 * 15
    assert math.isclose(drChild3.y2[8], 1.5+20, rel_tol=1e-4) # 0.1 * 15 + 0.4 * 50
    assert math.isclose(drChild3.y2[9], 5, rel_tol=1e-4) # 0.1 * 50
    assert math.isclose(drChild3.y2[10], 15, rel_tol=1e-4) # 0.3 * 50
    assert math.isclose(drChild3.y2[11], 10+2, rel_tol=1e-4) # 0.2 * 50 + 0.2 * 10
    assert math.isclose(drChild3.y2[12], 8+54, rel_tol=1e-4) # 0.8 * 10 + 0.9 * 60
    assert math.isclose(drChild3.y2[13], 6, rel_tol=1e-4) # 0.1 * 60 
    assert math.isclose(drChild3.y2[14], 0.0, rel_tol=1e-4) 
    assert math.isclose(drChild3.y2[15], 9.6, rel_tol=1e-4)