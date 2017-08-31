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


def test_download_file(temp_dir, sample_gs_file):
    output_path = os.path.join(temp_dir, os.path.basename(sample_gs_file))
    GoogleStorage(sample_gs_file).download(output_path)
    actual = LocalFileStorage(temp_dir).list(relative=True)
    expected = ['foo.tar.gz', ]
    assert sorted(actual) == sorted(expected)
