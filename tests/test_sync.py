import pytest
import os
import time

from backports.tempfile import TemporaryDirectory

from stored import sync, list_files


@pytest.fixture
def sample_local_targz_url():
    return 'tests/files/foo.tar.gz'


@pytest.fixture
def sample_local_zip_url():
    return 'tests/files/foo.zip'


@pytest.fixture
def sample_local_dir(sample_local_targz_url):
    with TemporaryDirectory() as temp_dir:
        sync(sample_local_targz_url, temp_dir)
        yield temp_dir


def touch(path):
    with open(path, 'a'):
        os.utime(path, None)


def test_sync_to_file(temp_dir, sample_local_dir):
    input_path = os.path.join(sample_local_dir, 'foo.txt')
    output_path = os.path.join(temp_dir, 'foo.txt')
    touch(input_path)
    sync(input_path, output_path)
    actual = list_files(temp_dir, relative=True)
    expected = ['foo.txt', ]
    assert sorted(actual) == sorted(expected)


def test_sync_to_same_files_noop(sample_local_dir):
    input_path = os.path.join(sample_local_dir, 'foo.txt')
    touch(input_path)
    output_path = input_path
    output_last_modified = os.path.getmtime(output_path)
    time.sleep(1)
    sync(input_path, output_path)
    assert os.path.getmtime(output_path) == output_last_modified


def test_sync_to_dirs(temp_dir, sample_local_dir):
    sync(sample_local_dir, temp_dir)
    actual = list_files(temp_dir, relative=True)
    expected = ['bar.txt', 'baz/foo.txt']
    assert sorted(actual) == sorted(expected)


def test_sync_to_archives_without_unzip(temp_dir, sample_local_zip_url):
    temp_file = os.path.join(temp_dir, os.path.basename(sample_local_zip_url))
    sync(sample_local_zip_url, temp_file)
    actual = list_files(temp_dir, relative=True)
    expected = ['foo.zip']
    assert sorted(actual) == sorted(expected)


def test_sync_to_dirs_some_existing_files(temp_dir, sample_local_dir):
    bar_path = os.path.join(temp_dir, 'bar.txt')
    touch(bar_path)
    bar_last_modified = os.path.getmtime(bar_path)
    actual = list_files(temp_dir, relative=True)
    assert actual == ['bar.txt']

    sync(sample_local_dir, temp_dir)
    actual = list_files(temp_dir, relative=True)
    expected = ['bar.txt', 'baz/foo.txt']
    assert sorted(actual) == sorted(expected)

    assert os.path.getmtime(bar_path) == bar_last_modified


def test_sync_to_same_dirs(temp_dir):
    foo_path = os.path.join(temp_dir, 'foo.txt')
    touch(foo_path)

    foo_last_modified = os.path.getmtime(foo_path)
    before = list_files(temp_dir, relative=True)
    assert before == ['foo.txt']

    sync(temp_dir, temp_dir)
    after = list_files(temp_dir, relative=True)
    assert after == ['foo.txt']

    assert os.path.getmtime(foo_path) == foo_last_modified


def test_sync_to_and_extract_targz(temp_dir, sample_local_targz_url):
    sync(sample_local_targz_url, temp_dir)
    actual = list_files(temp_dir, relative=True)
    expected = ['bar.txt', 'baz/foo.txt']
    assert sorted(actual) == sorted(expected)


def test_sync_to_and_extract_zip(temp_dir, sample_local_zip_url):
    sync(sample_local_zip_url, temp_dir)
    actual = list_files(temp_dir, relative=True)
    expected = ['bar.txt', 'baz/foo.txt']
    assert sorted(actual) == sorted(expected)


def test_and_sync_to_with_archive(temp_dir, sample_local_dir):
    output_path = os.path.join(temp_dir, 'foo.zip')
    sync(sample_local_dir, output_path)
    assert os.path.isfile(output_path)
