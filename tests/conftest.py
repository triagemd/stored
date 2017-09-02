import pytest

from tempfile import NamedTemporaryFile
from backports.tempfile import TemporaryDirectory


@pytest.fixture(scope='function')
def temp_dir():
    with TemporaryDirectory() as d:
        yield d


@pytest.fixture(scope='function')
def temp_file():
    with NamedTemporaryFile() as f:
        yield f.name
