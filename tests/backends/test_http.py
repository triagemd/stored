import pytest
import os

from stored.backends.local import LocalFileStorage
from stored.backends.http import HTTPStorage


@pytest.fixture
def sample_https_url():
    return 'https://storage.googleapis.com/stored-http-01de4705-5b30-4631-b04e-c987c1476c4a/foo.tar.gz'


@pytest.fixture
def sample_http_url():
    return 'http://storage.googleapis.com/stored-http-01de4705-5b30-4631-b04e-c987c1476c4a/foo.tar.gz'


def test_sync_to_file_from_https(temp_dir, sample_https_url):
    output_path = os.path.join(temp_dir, os.path.basename(sample_https_url))
    HTTPStorage(sample_https_url).sync_to(output_path)
    actual = LocalFileStorage(temp_dir).list(relative=True)
    expected = ['foo.tar.gz', ]
    assert sorted(actual) == sorted(expected)


def test_sync_to_file_from_http(temp_dir, sample_http_url):
    output_path = os.path.join(temp_dir, os.path.basename(sample_http_url))
    HTTPStorage(sample_http_url).sync_to(output_path)
    actual = LocalFileStorage(temp_dir).list(relative=True)
    expected = ['foo.tar.gz', ]
    assert sorted(actual) == sorted(expected)


def test_list(temp_dir):
    with pytest.raises(NotImplementedError):
        HTTPStorage('foo').list()


def test_list_relative(temp_dir):
    with pytest.raises(NotImplementedError):
        HTTPStorage('foo').list(relative=True)
