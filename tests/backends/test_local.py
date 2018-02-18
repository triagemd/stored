import pytest
import os

from backports.tempfile import TemporaryDirectory

from stored.backends.local import LocalFileStorage


@pytest.fixture
def sample_local_path():
    return 'tests/files/foo.tar.gz'


def touch(path):
    with open(path, 'a'):
        os.utime(path, None)


def test_sync_to_file(temp_dir, sample_local_path):
    output_path = os.path.join(temp_dir, os.path.basename(sample_local_path))
    LocalFileStorage(sample_local_path).sync_to(output_path)
    actual = LocalFileStorage(temp_dir).list(relative=True)
    expected = ['foo.tar.gz', ]
    assert sorted(actual) == sorted(expected)


def test_sync_to_file_nonexistent_input(temp_dir):
    output_path = os.path.join(temp_dir, 'nonexistent_file')
    LocalFileStorage('nonexistent_file').sync_to(output_path)
    actual = LocalFileStorage(temp_dir).list(relative=True)
    expected = []
    assert sorted(actual) == sorted(expected)


def test_sync_to_directory(temp_dir):
    with TemporaryDirectory() as input_dir:
        touch(os.path.join(input_dir, 'foo.txt'))
        os.makedirs(os.path.join(input_dir, 'bar'))
        touch(os.path.join(input_dir, 'bar', 'baz.txt'))
        LocalFileStorage(input_dir).sync_to(temp_dir)
    actual = LocalFileStorage(temp_dir).list(relative=True)
    expected = ['foo.txt', 'bar/baz.txt']
    assert sorted(actual) == sorted(expected)


def test_sync_to_directory_creates_output_dir(temp_dir):
    output_dir = os.path.join(temp_dir, 'inner_dir')
    with TemporaryDirectory() as input_dir:
        touch(os.path.join(input_dir, 'foo.txt'))
        os.makedirs(os.path.join(input_dir, 'bar'))
        touch(os.path.join(input_dir, 'bar', 'baz.txt'))
        LocalFileStorage(input_dir).sync_to(output_dir)
    actual = LocalFileStorage(temp_dir).list(relative=True)
    expected = ['inner_dir/foo.txt', 'inner_dir/bar/baz.txt']
    assert sorted(actual) == sorted(expected)


def test_sync_to_directory_nonexistent_input(temp_dir):
    LocalFileStorage('nonexistent_dir').sync_to(temp_dir)
    actual = LocalFileStorage(temp_dir).list(relative=True)
    expected = []
    assert sorted(actual) == sorted(expected)


def test_sync_from_directory(temp_dir, sample_local_path):
    with TemporaryDirectory() as input_dir:
        touch(os.path.join(input_dir, 'foo.txt'))
        os.makedirs(os.path.join(input_dir, 'bar'))
        touch(os.path.join(input_dir, 'bar', 'baz.txt'))
        LocalFileStorage(temp_dir).sync_from(input_dir)
    actual = LocalFileStorage(temp_dir).list(relative=True)
    expected = ['foo.txt', 'bar/baz.txt']
    assert sorted(actual) == sorted(expected)


def test_sync_from_directory_nonexistent_input(temp_dir):
    LocalFileStorage(temp_dir).sync_from('nonexistent_dir')
    actual = LocalFileStorage(temp_dir).list(relative=True)
    expected = []
    assert sorted(actual) == sorted(expected)


def test_sync_from_file(temp_dir, sample_local_path):
    output_path = os.path.join(temp_dir, os.path.basename(sample_local_path))
    LocalFileStorage(output_path).sync_from(sample_local_path)
    actual = LocalFileStorage(temp_dir).list(relative=True)
    expected = ['foo.tar.gz', ]
    assert sorted(actual) == sorted(expected)


def test_sync_from_file_nonexistent_input(temp_dir):
    output_path = os.path.join(temp_dir, 'nonexistent_file')
    LocalFileStorage(output_path).sync_from('nonexistent_file')
    actual = LocalFileStorage(temp_dir).list(relative=True)
    expected = []
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


def test_is_dir(sample_local_path):
    assert LocalFileStorage(os.path.dirname(sample_local_path)).is_dir()
    assert not LocalFileStorage(sample_local_path).is_dir()
    assert LocalFileStorage(sample_local_path + '/').is_dir()
    assert LocalFileStorage(sample_local_path + '/foo').is_dir()


def test_filename():
    assert LocalFileStorage('/foo/bar.zip').filename == 'bar.zip'
