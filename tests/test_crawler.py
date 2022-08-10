from pathlib import Path

from anadet.crawler import Crawler

from tests.config import BASE_DIR

def test_file_crawler_class_exists():
    assert BASE_DIR.joinpath("anadet/crawler.py").is_file()

def test_crawl_test_dir():
    cr = Crawler(BASE_DIR.joinpath('tests/test_resources/tests_1'))
    files = cr.getFiles()

    names = [i.name for i in files]
    assert 'results-master_h1_DiagDetPV-3-Spec.csv' in names
    assert 'results-master_h1_XWallDetPV-6-Theta.csv' in names
    assert 'results-master_h1_DiagDetPV-2-Phi.csv' in names
    assert 'results-master_h1_VertDetPV-8-Phi.csv' in names
    assert 'not_tracked_file.csv' not in names