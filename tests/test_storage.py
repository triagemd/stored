import pytest
import os
import time

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
        Storage(sample_local_targz_url).sync_to(temp_dir)
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


def test_sync_to_file(temp_dir, sample_local_dir):
    input_path = os.path.join(sample_local_dir, 'foo.txt')
    output_path = os.path.join(temp_dir, 'foo.txt')
    touch(input_path)
    Storage(input_path).sync_to(output_path)
    actual = Storage(temp_dir).list(relative=True)
    expected = ['foo.txt', ]
    assert sorted(actual) == sorted(expected)


def test_sync_to_same_files_noop(sample_local_dir):
    input_path = os.path.join(sample_local_dir, 'foo.txt')
    touch(input_path)
    output_path = input_path
    output_last_modified = os.path.getmtime(output_path)
    time.sleep(1)
    Storage(input_path).sync_to(output_path)
    assert os.path.getmtime(output_path) == output_last_modified


def test_sync_to_dirs(temp_dir, sample_local_dir):
    Storage(sample_local_dir).sync_to(temp_dir)
    actual = Storage(temp_dir).list(relative=True)
    expected = ['bar.txt', 'baz/foo.txt']
    assert sorted(actual) == sorted(expected)


def test_sync_to_dirs_some_existing_files(temp_dir, sample_local_dir):
    bar_path = os.path.join(temp_dir, 'bar.txt')
    touch(bar_path)
    bar_last_modified = os.path.getmtime(bar_path)
    actual = Storage(temp_dir).list(relative=True)
    assert actual == ['bar.txt']

    Storage(sample_local_dir).sync_to(temp_dir)
    actual = Storage(temp_dir).list(relative=True)
    expected = ['bar.txt', 'baz/foo.txt']
    assert sorted(actual) == sorted(expected)

    assert os.path.getmtime(bar_path) == bar_last_modified


def test_sync_to_same_dirs(temp_dir):
    foo_path = os.path.join(temp_dir, 'foo.txt')
    touch(foo_path)

    foo_last_modified = os.path.getmtime(foo_path)
    before = Storage(temp_dir).list(relative=True)
    assert before == ['foo.txt']

    Storage(temp_dir).sync_to(temp_dir)
    after = Storage(temp_dir).list(relative=True)
    assert after == ['foo.txt']

    assert os.path.getmtime(foo_path) == foo_last_modified


def test_sync_to_and_extract_targz(temp_dir, sample_local_targz_url):
    Storage(sample_local_targz_url).sync_to(temp_dir)
    actual = Storage(temp_dir).list(relative=True)
    expected = ['bar.txt', 'baz/foo.txt']
    assert sorted(actual) == sorted(expected)


def test_sync_to_and_extract_zip(temp_dir, sample_local_zip_url):
    Storage(sample_local_zip_url).sync_to(temp_dir)
    actual = Storage(temp_dir).list(relative=True)
    expected = ['bar.txt', 'baz/foo.txt']
    assert sorted(actual) == sorted(expected)


def test_and_sync_from_with_archive(temp_dir, sample_local_dir):
    output_path = os.path.join(temp_dir, 'foo.zip')
    Storage(output_path).sync_from(sample_local_dir)
    assert os.path.exists(output_path)
