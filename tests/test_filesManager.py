from pathlib import Path

from anadet.filesManager import FilesManager

BASE_DIR = Path(__file__).resolve().parent.parent

def test_filesManagerRead():
    fm = FilesManager()
    fm.readDirectory(BASE_DIR.joinpath('tests/test_resources'))
    assert len(fm.metaFiles) == 2
    assert len(fm.detectorFiles) == 4