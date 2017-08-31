import pytest

from stored import Archive, Storage


@pytest.fixture
def sample_targz_file():
    with open('tests/files/foo.tar.gz', 'rb') as file:
        return file


@pytest.fixture
def sample_zip_file():
    with open('tests/files/foo.zip', 'rb') as file:
        return file


def test_extract_targz_from_http(temp_dir, sample_targz_file):
    Archive(sample_targz_file).extract(temp_dir)
    actual = Storage(temp_dir).list_files(relative=True)
    expected = ['bar.txt', 'baz/foo.txt']
    assert sorted(actual) == sorted(expected)


def test_extract_zip_from_http(temp_dir, sample_zip_file):
    Archive(sample_zip_file).extract(temp_dir)
    actual = Storage(temp_dir).list_files(relative=True)
    expected = ['bar.txt', 'baz/foo.txt']
    assert sorted(actual) == sorted(expected)
