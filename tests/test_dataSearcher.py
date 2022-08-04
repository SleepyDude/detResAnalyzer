from anadet.dataSearcher import DataSearcher
import math

def test_lookForEnergy():
    dm = DataSearcher()
    filename = "test_resources/2 MeV 4kk/results-master_h1_DiagDetPV-2-Phi.csv"
    res = dm.lookingForEnergyInfo(filename)
    assert len(res) == 1
    first = res[0]
    assert math.isclose(first['energy'], 2.0, rel_tol=1e-4) and first['energy_unit'] == 'MeV',\
        "One energy with unit found"

    filename = "test_resources 3keV/14 MeV 4kk/testtest 15.45 PeV results-master_h1_DiagDetPV-2-Phi-8.11eV.csv"
    res = dm.lookingForEnergyInfo(filename)
    assert len(res) == 3
    assert math.isclose(res[0]['energy'], 3.0, rel_tol=1e-4) and res[0]['energy_unit'] == 'keV'
    assert math.isclose(res[1]['energy'], 14.0, rel_tol=1e-4) and res[1]['energy_unit'] == 'MeV'
    assert math.isclose(res[2]['energy'], 8.11, rel_tol=1e-4) and res[2]['energy_unit'] == 'eV'

    filename = "test_resources 3leV/4kk/results-master_h1_DiagDetPV-2-Phi.csv"
    res = dm.lookingForEnergyInfo(filename)
    assert len(res) == 0

def test_lookForNhists():
    dm = DataSearcher()
    filename = "test_resources 3keV/14 MeV 4kk/testtest 15.45 PeV results-master_h1_DiagDetPV-2-Phi-8.11eV.csv"
    res = dm.lookingForNhists(filename)
    assert res == 4e+6

    filename = "test_resources/14 MeV/testtest_25kkk/results-master_h1_DiagDetPV-2-Phi-8.11eV.csv"
    res = dm.lookingForNhists(filename)
    assert res == 25e+9
