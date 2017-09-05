import os


from stored import list_files


def touch(path):
    with open(path, 'a'):
        os.utime(path, None)


def test_list_files(temp_dir):
    touch(os.path.join(temp_dir, 'foo.jpg'))
    os.makedirs(os.path.join(temp_dir, 'bar'))
    touch(os.path.join(temp_dir, 'bar', 'baz-1.jpg'))
    touch(os.path.join(temp_dir, 'bar', 'baz-2.jpg'))
    actual = list_files(temp_dir)
    actual = [file.replace(temp_dir + '/', '') for file in actual]
    expected = ['foo.jpg', 'bar/baz-1.jpg', 'bar/baz-2.jpg']
    assert actual == expected


def test_list_files_relative(temp_dir):
    touch(os.path.join(temp_dir, 'foo.jpg'))
    os.makedirs(os.path.join(temp_dir, 'bar'))
    touch(os.path.join(temp_dir, 'bar', 'baz-1.jpg'))
    touch(os.path.join(temp_dir, 'bar', 'baz-2.jpg'))
    actual = list_files(temp_dir)
    expected = ['foo.jpg', 'bar/baz-1.jpg', 'bar/baz-2.jpg']
    assert actual == expected
