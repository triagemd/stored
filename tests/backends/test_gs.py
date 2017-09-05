import pytest
import os

from stored.backends.local import LocalFileStorage
from stored.backends.gs import GoogleStorage


@pytest.fixture
def sample_gs_dir():
    return 'gs://stored-gs-5d45f99e-77ba-4b79-a0d5-12b1d4608ec6'


@pytest.fixture
def sample_gs_file():
    return 'gs://stored-gs-5d45f99e-77ba-4b79-a0d5-12b1d4608ec6/foo.tar.gz'


def test_list(sample_gs_dir):
    actual = GoogleStorage(sample_gs_dir).list()
    expected = [
        'gs://stored-gs-5d45f99e-77ba-4b79-a0d5-12b1d4608ec6/foo.zip',
        'gs://stored-gs-5d45f99e-77ba-4b79-a0d5-12b1d4608ec6/foo.tar.gz'
    ]
    assert sorted(actual) == sorted(expected)


def test_list_relative(sample_gs_dir):
    actual = GoogleStorage(sample_gs_dir).list(relative=True)
    expected = ['foo.zip', 'foo.tar.gz']
    assert sorted(actual) == sorted(expected)


def test_sync_to_file(temp_dir, sample_gs_file):
    output_path = os.path.join(temp_dir, os.path.basename(sample_gs_file))
    GoogleStorage(sample_gs_file).sync_to(output_path)
    actual = LocalFileStorage(temp_dir).list(relative=True)
    expected = ['foo.tar.gz', ]
    assert sorted(actual) == sorted(expected)


def test_sync_to_directory(temp_dir, sample_gs_dir):
    GoogleStorage(sample_gs_dir).sync_to(temp_dir)
    actual = LocalFileStorage(temp_dir).list(relative=True)
    expected = ['foo.tar.gz', 'foo.zip']
    assert sorted(actual) == sorted(expected)

def test_is_dir(sample_gs_dir):
    assert GoogleStorage(sample_gs_dir).is_dir()
    assert not GoogleStorage(os.path.join(sample_gs_dir, 'foo.zip')).is_dir()
    assert GoogleStorage(os.path.join(sample_gs_dir, 'foo.zip/')).is_dir()
