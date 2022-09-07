from cmath import inf
import pytest
import math
from .config import BASE_DIR
from pathlib import Path
from ..anadet.detRes import DetRes


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
    assert dr.stat.nhists == 35e+6
    assert len(dr.origin_sequence) == 3
    first_words = [i.split()[0] for i in dr.origin_sequence]
    first_words_right = ['APPEND:', 'APPEND:', 'APPEND:']
    assert ''.join(first_words) == ''.join(first_words_right)

def test_statisticsCalculate():
    dr = DetRes()
    TEST_DIR = BASE_DIR.joinpath('tests/test_resources/filenames_and_grouping')
    fname = str( TEST_DIR.joinpath('1 keV 6kk/someName_h1_SpecDetDiag-2.csv') )
    dr.readDataFromCSV(fname)
    assert dr.stat.delta_max == -inf
    assert dr.stat.delta_min == inf
    assert dr.stat.has_calculated == False
    dr.calculateStatistics()
    assert len(dr.stat.means) == len(dr.stat.variances) == len(dr.stat.st_devs) == len(dr.y) == len(dr.y2) == 10
    assert math.isclose(dr.stat.means[0], 1.02609e-4, rel_tol=1e-4)
    assert math.isclose(dr.stat.means[9], 3.890283333e-5, rel_tol=1e-4)
    assert math.isclose(dr.stat.variances[0], 7.32211e-3, rel_tol=1e-4)
    assert math.isclose(dr.stat.variances[9], 2.80447e-3, rel_tol=1e-4)
    assert math.isclose(dr.stat.st_devs[0], 3.49335e-5, rel_tol=1e-4)
    assert math.isclose(dr.stat.st_devs[9], 2.16197e-5, rel_tol=1e-4)
    assert math.isclose(dr.stat.deltas[0], 3.40453e-1, rel_tol=1e-4)
    assert math.isclose(dr.stat.deltas[9], 5.55736e-1, rel_tol=1e-4)
    assert dr.stat.has_calculated == True
    
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

def test_createChild_3():
    test_data = {}
    test_data["y"] = [1,2,3,4,5,6,7,8,9,8,7,6,5,4,3,2,1] # len = 17
    test_data["y2"] = [9,8,7,6,5,4,3,2,1,2,3,4,5,6,7,8,9]
    # bin i                 0     1     2      3      4      5      6      7      8      9     10     11     12     13     14     15     16     17 
    test_data["bins"] = [1.23, 4.56, 7.89, 10.11, 12.13, 14.15, 16.17, 18.19, 20.21, 22.23, 24.25, 26.27, 28.29, 30.31, 32.33, 34.35, 36.37, 38.39]
    test_data["overflow_bot"] = 5.67
    test_data["overflow_top"] = 1.34
    test_data["nhists"] = 10e+6
    test_data["origin"] = "MANUALY CREATED from test_data in test_createChild_3"
    
    dr = DetRes()
    dr.setData(**test_data)

    shrink_bin = test_data["bins"][::2]
    ch = dr.createChild(shrink_bin)
    assert ch.stat.nhists == 1e+7
    assert len(ch.y) == 8
    assert len(ch.BINS[ch.bin_index]) == 9
    assert math.isclose(ch.overflow_bot, 5.67, abs_tol=1e-14)
    assert math.isclose(ch.overflow_top, 2.34, abs_tol=1e-14)
    assert math.isclose(ch.y[0], 3, abs_tol=1e-14)
    assert math.isclose(ch.y[1], 7, abs_tol=1e-14)
    assert math.isclose(ch.y[2], 11, abs_tol=1e-14)
    assert math.isclose(ch.y[3], 15, abs_tol=1e-14)
    assert math.isclose(ch.y[4], 17, abs_tol=1e-14)
    assert math.isclose(ch.y[5], 13, abs_tol=1e-14)
    assert math.isclose(ch.y[6], 9, abs_tol=1e-14)
    assert math.isclose(ch.y[7], 5, abs_tol=1e-14)

def test_strip():
    test_data = {}
    test_data["y"] = [0,0,0,4,5,6,7,8,9,8,7,6,5,0,0,0,0] # len = 17
    test_data["y2"] = [0,0,0,6,5,4,3,2,1,2,3,4,5,0,0,0,0]
    # bin i                 0     1     2     3*      4      5      6      7      8      9     10     11     12    13*     14     15     16     17 
    test_data["bins"] = [1.23, 4.56, 7.89, 10.11, 12.13, 14.15, 16.17, 18.19, 20.21, 22.23, 24.25, 26.27, 28.29, 30.31, 32.33, 34.35, 36.37, 38.39]
    test_data["overflow_bot"] = 5.67
    test_data["overflow_top"] = 1.34
    test_data["nhists"] = 10e+6
    test_data["origin"] = "MANUALY CREATED from test_data in test_strip()"
    
    dr = DetRes()
    dr.setData(**test_data)

    ch = dr.strip()
    print(ch.BINS[ch.bin_index])
    assert len(ch.BINS[ch.bin_index]) == 11
    assert len(ch.y) == 10
    assert math.isclose(ch.BINS[ch.bin_index][0], 10.11, abs_tol=1e-14)
    assert math.isclose(ch.BINS[ch.bin_index][1], 12.13, abs_tol=1e-14)
    assert math.isclose(ch.BINS[ch.bin_index][10], 30.31, abs_tol=1e-14)

    assert math.isclose(ch.y[0], dr.y[3], abs_tol=1e-14)
    assert math.isclose(ch.y[1], dr.y[4], abs_tol=1e-14)
    assert math.isclose(ch.y[9], dr.y[12], abs_tol=1e-14)

    assert math.isclose(ch.y2[0], dr.y2[3], abs_tol=1e-14)
    assert math.isclose(ch.y2[1], dr.y2[4], abs_tol=1e-14)
    assert math.isclose(ch.y2[9], dr.y2[12], abs_tol=1e-14)

def test_shrinkToDelta():
    dr = DetRes()
    TEST_DIR = BASE_DIR.joinpath('tests/test_resources/shrinkTest')
    fname = str(TEST_DIR.joinpath("100 keV 15kk 8/results-master_h1_VertDetPV-1-Spec.csv"))
    dr.readDataFromCSV(fname)
    assert len(dr.BINS[dr.bin_index]) == 501
    assert len(dr.y) == 500
    assert math.isclose(dr.BINS[dr.bin_index][3], 1.19916e-12, abs_tol=1e-14)
    assert math.isclose(dr.y[95], 400.511, abs_tol=1e-14)
    assert math.isclose(dr.y2[95], 22938, abs_tol=1e-14)
    
    dr.calculateStatistics()
    ch = dr.shrinkToDelta(0.1)
    assert ch.stat.delta_max <= 0.1 # rel. mistake less than 10% in every bin
    assert len(ch.BINS[ch.bin_index]) == 306
    assert len(ch.y) == 305
    bP = dr.BINS[dr.bin_index]
    bC = ch.BINS[ch.bin_index]
    assert math.isclose(bP[0], bC[0], abs_tol=1e-14)
    assert math.isclose(bP[103], bC[1], abs_tol=1e-14)
    assert math.isclose(bP[109], bC[2], abs_tol=1e-14)
    assert math.isclose(bP[113], bC[3], abs_tol=1e-14)
    assert math.isclose(bP[116], bC[4], abs_tol=1e-14)
    assert math.isclose(bP[118], bC[5], abs_tol=1e-14)
    assert math.isclose(bP[120], bC[6], abs_tol=1e-14)
    assert math.isclose(bP[122], bC[7], abs_tol=1e-14)
    assert math.isclose(bP[123], bC[8], abs_tol=1e-14)
    assert math.isclose(bP[124], bC[9], abs_tol=1e-14)
    assert math.isclose(bP[125], bC[10], abs_tol=1e-14)

    assert math.isclose(ch.y[0], 7364.39648, abs_tol=1e-14)
    assert math.isclose(ch.y[1], 8701.235, abs_tol=1e-14)
    assert math.isclose(ch.y[2], 9749.82, abs_tol=1e-14)
    assert math.isclose(ch.y[3], 10828.34, abs_tol=1e-14)
    assert math.isclose(ch.y[4], 9140.85, abs_tol=1e-14)
    assert math.isclose(ch.y[5], 11809.42, abs_tol=1e-14)
    assert math.isclose(ch.y[6], 14910.89, abs_tol=1e-14)
    assert math.isclose(ch.y[7], dr.y[122], abs_tol=1e-14)
    assert math.isclose(ch.y[8], dr.y[123], abs_tol=1e-14)
    assert math.isclose(ch.y[9], dr.y[124], abs_tol=1e-14)
    assert math.isclose(ch.y[10], dr.y[125], abs_tol=1e-14)
    assert math.isclose(ch.y[-1], 0, abs_tol=1e-14)

    assert math.isclose(ch.y2[0], 528899.9598, abs_tol=1e-14)
    assert math.isclose(ch.y2[1], 625568.4, abs_tol=1e-14)
    assert math.isclose(ch.y2[2], 720508, abs_tol=1e-14)
    assert math.isclose(ch.y2[3], 791811, abs_tol=1e-14)
    assert math.isclose(ch.y2[4], 683847, abs_tol=1e-14)
    assert math.isclose(ch.y2[5], 856573, abs_tol=1e-14)
    assert math.isclose(ch.y2[6], 1094181, abs_tol=1e-14)
    assert math.isclose(ch.y2[7], dr.y2[122], abs_tol=1e-14)
    assert math.isclose(ch.y2[8], dr.y2[123], abs_tol=1e-14)
    assert math.isclose(ch.y2[9], dr.y2[124], abs_tol=1e-14)
    assert math.isclose(ch.y2[10], dr.y2[125], abs_tol=1e-14)

def test_strip_and_shrink():
    dr = DetRes()
    TEST_DIR = BASE_DIR.joinpath('tests/test_resources/shrinkTest')
    fname = str(TEST_DIR.joinpath("100 keV 15kk 8/results-master_h1_VertDetPV-1-Spec.csv"))
    dr.readDataFromCSV(fname)
    assert len(dr.BINS[dr.bin_index]) == 501
    assert len(dr.y) == 500
    assert math.isclose(dr.BINS[dr.bin_index][3], 1.19916e-12, abs_tol=1e-14)
    assert math.isclose(dr.y[95], 400.511, abs_tol=1e-14)
    assert math.isclose(dr.y2[95], 22938, abs_tol=1e-14)
    
    dr.calculateStatistics()
    ch = dr.strip()
    ch = ch.shrinkToDelta(0.1)
    assert ch.stat.delta_max <= 0.1 # rel. mistake less than 10% in every bin
    assert len(ch.BINS[ch.bin_index]) == 305
    assert len(ch.y) == 304
    bP = dr.BINS[dr.bin_index]
    bC = ch.BINS[ch.bin_index]
    assert math.isclose(bP[33], bC[0], abs_tol=1e-14)
    assert math.isclose(bP[103], bC[1], abs_tol=1e-14)
    assert math.isclose(bP[109], bC[2], abs_tol=1e-14)
    assert math.isclose(bP[113], bC[3], abs_tol=1e-14)
    assert math.isclose(bP[116], bC[4], abs_tol=1e-14)
    assert math.isclose(bP[118], bC[5], abs_tol=1e-14)
    assert math.isclose(bP[120], bC[6], abs_tol=1e-14)
    assert math.isclose(bP[122], bC[7], abs_tol=1e-14)
    assert math.isclose(bP[123], bC[8], abs_tol=1e-14)
    assert math.isclose(bP[124], bC[9], abs_tol=1e-14)
    assert math.isclose(bP[125], bC[10], abs_tol=1e-14)

    assert math.isclose(ch.y[0], 7364.39648, abs_tol=1e-14)
    assert math.isclose(ch.y[1], 8701.235, abs_tol=1e-14)
    assert math.isclose(ch.y[2], 9749.82, abs_tol=1e-14)
    assert math.isclose(ch.y[3], 10828.34, abs_tol=1e-14)
    assert math.isclose(ch.y[4], 9140.85, abs_tol=1e-14)
    assert math.isclose(ch.y[5], 11809.42, abs_tol=1e-14)
    assert math.isclose(ch.y[6], 14910.89, abs_tol=1e-14)
    assert math.isclose(ch.y[7], dr.y[122], abs_tol=1e-14)
    assert math.isclose(ch.y[8], dr.y[123], abs_tol=1e-14)
    assert math.isclose(ch.y[9], dr.y[124], abs_tol=1e-14)
    assert math.isclose(ch.y[10], dr.y[125], abs_tol=1e-14)

    assert math.isclose(ch.y2[0], 528899.9598, abs_tol=1e-14)
    assert math.isclose(ch.y2[1], 625568.4, abs_tol=1e-14)
    assert math.isclose(ch.y2[2], 720508, abs_tol=1e-14)
    assert math.isclose(ch.y2[3], 791811, abs_tol=1e-14)
    assert math.isclose(ch.y2[4], 683847, abs_tol=1e-14)
    assert math.isclose(ch.y2[5], 856573, abs_tol=1e-14)
    assert math.isclose(ch.y2[6], 1094181, abs_tol=1e-14)
    assert math.isclose(ch.y2[7], dr.y2[122], abs_tol=1e-14)
    assert math.isclose(ch.y2[8], dr.y2[123], abs_tol=1e-14)
    assert math.isclose(ch.y2[9], dr.y2[124], abs_tol=1e-14)
    assert math.isclose(ch.y2[10], dr.y2[125], abs_tol=1e-14)

def test_dump_to_file():
    dr = DetRes()
    TEST_DIR = BASE_DIR.joinpath('tests/test_resources/shrinkTest')
    fname = str(TEST_DIR.joinpath("100 keV 15kk 8/results-master_h1_VertDetPV-1-Spec.csv"))
    dr.readDataFromCSV(fname)
    ch = dr.strip().shrinkToDelta(0.1)
    dump_fname = str(BASE_DIR.joinpath('tests/test_resources/dump_data/res.txt'))
    ch.dumpToFile(dump_fname)
    assert Path(dump_fname).is_file()
    