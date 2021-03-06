import pytest
import os

from backports.tempfile import TemporaryDirectory

from stored import Archive, sync, list_files


@pytest.fixture
def sample_targz_path():
    return 'tests/files/foo.tar.gz'


@pytest.fixture
def sample_zip_path():
    return 'tests/files/foo.zip'


@pytest.fixture
def sample_local_dir():
    with TemporaryDirectory() as temp_dir:
        sync('tests/files/foo.tar.gz', temp_dir)
        yield temp_dir


def test_extract_targz(temp_dir, sample_targz_path):
    Archive(sample_targz_path).extract(temp_dir)
    actual = list_files(temp_dir, relative=True)
    expected = ['bar.txt', 'baz/foo.txt']
    assert sorted(actual) == sorted(expected)


def test_extract_zip(temp_dir, sample_zip_path):
    Archive(sample_zip_path).extract(temp_dir)
    actual = list_files(temp_dir, relative=True)
    expected = ['bar.txt', 'baz/foo.txt']
    assert sorted(actual) == sorted(expected)


def test_create_zip(temp_dir, sample_local_dir):
    output_file = os.path.join(temp_dir, 'foo.zip')
    Archive(output_file).create(sample_local_dir)
    assert os.path.exists(output_file)
