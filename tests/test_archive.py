import pytest

from stored import Archive, Storage


@pytest.fixture
def sample_targz_path():
    return 'tests/files/foo.tar.gz'


@pytest.fixture
def sample_zip_path():
    return 'tests/files/foo.zip'


def test_extract_targz(temp_dir, sample_targz_path):
    Archive(sample_targz_path).extract(temp_dir)
    actual = Storage(temp_dir).list(relative=True)
    expected = ['bar.txt', 'baz/foo.txt']
    assert sorted(actual) == sorted(expected)


def test_extract_zip(temp_dir, sample_zip_path):
    Archive(sample_zip_path).extract(temp_dir)
    actual = Storage(temp_dir).list(relative=True)
    expected = ['bar.txt', 'baz/foo.txt']
    assert sorted(actual) == sorted(expected)
