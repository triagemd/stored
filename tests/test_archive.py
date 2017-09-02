import pytest
import os

from backports.tempfile import TemporaryDirectory

from stored import Archive, Storage


@pytest.fixture
def sample_targz_path():
    return 'tests/files/foo.tar.gz'


@pytest.fixture
def sample_zip_path():
    return 'tests/files/foo.zip'


@pytest.fixture
def sample_local_dir():
    with TemporaryDirectory() as temp_dir:
        Storage('tests/files/foo.tar.gz').sync_to(temp_dir, extract=True)
        yield temp_dir


def test_extract_targz(temp_dir, sample_targz_path):
    Archive(sample_targz_path).extract(temp_dir)
    actual = Storage(temp_dir).list(relative=True)
    expected = ['bar.txt', 'baz/foo.txt']
    assert sorted(actual) == sorted(expected)


def test_extract_zip(temp_dir, sample_zip_path):
    Archive(sample_zip_path).extract(temp_dir)
    actual = Storage(temp_dir).list(relative=True)
    expected = ['bar.txt', 'baz/foo.txt']
    assert sorted(actual) == sorted(expected)


def test_create_zip(temp_dir, sample_local_dir):
    output_file = os.path.join(temp_dir, 'foo.zip')
    Archive(output_file).create(sample_local_dir)
    assert os.path.exists(output_file)
