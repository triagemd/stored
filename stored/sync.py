import os

from backports.tempfile import TemporaryDirectory

from .archive import Archive
from .backends import get_backend, LocalFileStorage


def sync(input_path, output_path, force_unpack=False):
    input_storage = get_backend(input_path)
    output_storage = get_backend(output_path)

    if not isinstance(input_storage, LocalFileStorage) and not isinstance(output_storage, LocalFileStorage):
        raise ValueError('either input_path or output_path must be local file system')

    if input_path == output_path:
        return

    if (force_unpack or Archive(input_storage.filename).valid) and output_storage.is_dir():
        with TemporaryDirectory() as temp_dir:
            archive_path = os.path.join(temp_dir, input_storage.filename)
            input_storage.sync_to(archive_path)
            Archive(archive_path).extract(output_path, force_zip=force_unpack)
    elif Archive(output_storage.filename).valid and input_storage.is_dir():
        with TemporaryDirectory() as temp_dir:
            archive_path = os.path.join(temp_dir, output_storage.filename)
            Archive(archive_path).create(input_path)
            output_storage.sync_from(archive_path)
    else:
        input_storage.sync_to(output_path)
