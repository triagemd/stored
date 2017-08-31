import pytest
import os

from stored.backends.local import LocalFileStorage


@pytest.fixture
def sample_local_path():
    return 'tests/files/foo.tar.gz'


def touch(path):
    with open(path, 'a'):
        os.utime(path, None)


def test_download_file(temp_dir, sample_local_path):
    output_path = os.path.join(temp_dir, os.path.basename(sample_local_path))
    LocalFileStorage(sample_local_path).download(output_path)
    actual = LocalFileStorage(temp_dir).list(relative=True)
    expected = ['foo.tar.gz', ]
    assert sorted(actual) == sorted(expected)


def test_list(temp_dir):
    touch(os.path.join(temp_dir, 'foo.jpg'))
    os.makedirs(os.path.join(temp_dir, 'bar'))
    touch(os.path.join(temp_dir, 'bar', 'baz-1.jpg'))
    touch(os.path.join(temp_dir, 'bar', 'baz-2.jpg'))
    actual = LocalFileStorage(temp_dir).list()
    actual = [file.replace(temp_dir + '/', '') for file in actual]
    expected = ['foo.jpg', 'bar/baz-1.jpg', 'bar/baz-2.jpg']
    assert actual == expected


def test_list_relative(temp_dir):
    touch(os.path.join(temp_dir, 'foo.jpg'))
    os.makedirs(os.path.join(temp_dir, 'bar'))
    touch(os.path.join(temp_dir, 'bar', 'baz-1.jpg'))
    touch(os.path.join(temp_dir, 'bar', 'baz-2.jpg'))
    actual = LocalFileStorage(temp_dir).list(relative=True)
    expected = ['foo.jpg', 'bar/baz-1.jpg', 'bar/baz-2.jpg']
    assert actual == expected
