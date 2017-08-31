import pytest
import os

from backports.tempfile import TemporaryDirectory

from stored import Storage


@pytest.fixture
def sample_local_targz_url():
    return 'tests/files/foo.tar.gz'


@pytest.fixture
def sample_local_zip_url():
    return 'tests/files/foo.zip'


@pytest.fixture
def sample_local_dir(sample_local_targz_url):
    with TemporaryDirectory() as temp_dir:
        Storage(sample_local_targz_url).download(temp_dir, extract=True)
        yield temp_dir


def touch(path):
    with open(path, 'a'):
        os.utime(path, None)


def test_list_files(temp_dir):
    touch(os.path.join(temp_dir, 'foo.jpg'))
    os.makedirs(os.path.join(temp_dir, 'bar'))
    touch(os.path.join(temp_dir, 'bar', 'baz-1.jpg'))
    touch(os.path.join(temp_dir, 'bar', 'baz-2.jpg'))
    actual = Storage(temp_dir).list()
    actual = [file.replace(temp_dir + '/', '') for file in actual]
    expected = ['foo.jpg', 'bar/baz-1.jpg', 'bar/baz-2.jpg']
    assert actual == expected


def test_list_files_relative(temp_dir):
    touch(os.path.join(temp_dir, 'foo.jpg'))
    os.makedirs(os.path.join(temp_dir, 'bar'))
    touch(os.path.join(temp_dir, 'bar', 'baz-1.jpg'))
    touch(os.path.join(temp_dir, 'bar', 'baz-2.jpg'))
    actual = Storage(temp_dir).list(relative=True)
    expected = ['foo.jpg', 'bar/baz-1.jpg', 'bar/baz-2.jpg']
    assert actual == expected


def test_download_and_extract_targz(temp_dir, sample_local_targz_url):
    Storage(sample_local_targz_url).download(temp_dir, extract=True)
    actual = Storage(temp_dir).list(relative=True)
    expected = ['bar.txt', 'baz/foo.txt']
    assert sorted(actual) == sorted(expected)


def test_download_and_extract_zip(temp_dir, sample_local_zip_url):
    Storage(sample_local_zip_url).download(temp_dir, extract=True)
    actual = Storage(temp_dir).list(relative=True)
    expected = ['bar.txt', 'baz/foo.txt']
    assert sorted(actual) == sorted(expected)


def test_archive_and_upload(temp_dir, sample_local_dir):
    output_path = os.path.join(temp_dir, 'foo.zip')
    Storage(output_path).upload(sample_local_dir, archive=True)
    assert os.path.exists(output_path)
