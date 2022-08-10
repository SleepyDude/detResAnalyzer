from pathlib import Path

from anadet.filesManager import FilesManager
from tests.config import BASE_DIR

def test_filesManagerRead():
    fm = FilesManager()
    fm.readDirectory(BASE_DIR.joinpath('tests/test_resources/tests_1'))
    assert len(fm.metaFiles) == 1
    assert len(fm.detectorFiles) == 4
    