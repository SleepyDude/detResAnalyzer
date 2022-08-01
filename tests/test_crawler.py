from pathlib import Path

from anadet.crawler import Crawler

BASE_DIR = Path(__file__).resolve().parent.parent

def test_file_detector_class_exists():
    assert BASE_DIR.joinpath("anadet/crawler.py").is_file()


    