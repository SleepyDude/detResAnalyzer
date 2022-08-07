from anadet.metaReader import MetaReader
import math

def test_readMeta():
    metapath = "/Users/kolodinevgenij/projects/detector-res/detResAnalyzer/tests/test_resources/tests_1/meta.yaml"
    mr = MetaReader()
    mr.readFile(metapath)
    params = mr.getParamsForDetector('Vert', 5)
    assert math.isclose(params['distance'], 500, rel_tol=1e-4)
    assert math.isclose(params['angleView'], 0.002481405, rel_tol=1e-4)
    