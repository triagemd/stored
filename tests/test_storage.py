import pytest
import os

from stored import Storage


@pytest.fixture
def sample_https_model_targz_url():
    return 'https://storage.googleapis.com/stored-http-01de4705-5b30-4631-b04e-c987c1476c4a/foo.tar.gz'


@pytest.fixture
def sample_https_model_zip_url():
    return 'https://storage.googleapis.com/stored-http-01de4705-5b30-4631-b04e-c987c1476c4a/foo.zip'


@pytest.fixture
def sample_gs_model_targz_url():
    return 'gs://stored-gs-5d45f99e-77ba-4b79-a0d5-12b1d4608ec6/foo.tar.gz'


@pytest.fixture
def sample_gs_model_zip_url():
    return 'gs://stored-gs-5d45f99e-77ba-4b79-a0d5-12b1d4608ec6/foo.zip'


def touch(path):
    with open(path, 'a'):
        os.utime(path, None)


def test_download_and_extract_targz_from_http(temp_dir, sample_https_model_targz_url):
    Storage(sample_https_model_targz_url).download_and_extract(temp_dir)
    actual = Storage(temp_dir).list_files(relative=True)
    expected = ['bar.txt', 'baz/foo.txt']
    assert sorted(actual) == sorted(expected)


def test_download_and_extract_zip_from_http(temp_dir, sample_https_model_zip_url):
    Storage(sample_https_model_zip_url).download_and_extract(temp_dir)
    actual = Storage(temp_dir).list_files(relative=True)
    expected = ['bar.txt', 'baz/foo.txt']
    assert sorted(actual) == sorted(expected)


def test_download_and_extract_targz_from_gs(temp_dir, sample_gs_model_targz_url):
    Storage(sample_gs_model_targz_url).download_and_extract(temp_dir)
    actual = Storage(temp_dir).list_files(relative=True)
    expected = ['bar.txt', 'baz/foo.txt']
    assert sorted(actual) == sorted(expected)


def test_download_and_extract_zip_from_gs(temp_dir, sample_gs_model_zip_url):
    Storage(sample_gs_model_zip_url).download_and_extract(temp_dir)
    actual = Storage(temp_dir).list_files(relative=True)
    expected = ['bar.txt', 'baz/foo.txt']
    assert sorted(actual) == sorted(expected)


def test_list_files(temp_dir):
    touch(os.path.join(temp_dir, 'foo.jpg'))
    os.makedirs(os.path.join(temp_dir, 'bar'))
    touch(os.path.join(temp_dir, 'bar', 'baz-1.jpg'))
    touch(os.path.join(temp_dir, 'bar', 'baz-2.jpg'))
    actual = Storage(temp_dir).list_files()
    actual = [file.replace(temp_dir + '/', '') for file in actual]
    expected = ['foo.jpg', 'bar/baz-1.jpg', 'bar/baz-2.jpg']
    assert actual == expected


def test_list_files_relative(temp_dir):
    touch(os.path.join(temp_dir, 'foo.jpg'))
    os.makedirs(os.path.join(temp_dir, 'bar'))
    touch(os.path.join(temp_dir, 'bar', 'baz-1.jpg'))
    touch(os.path.join(temp_dir, 'bar', 'baz-2.jpg'))
    actual = Storage(temp_dir).list_files(relative=True)
    expected = ['foo.jpg', 'bar/baz-1.jpg', 'bar/baz-2.jpg']
    assert actual == expected
