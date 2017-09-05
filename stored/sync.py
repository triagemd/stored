import os

from backports.tempfile import TemporaryDirectory

from .archive import Archive
from .backends import get_backend, LocalFileStorage


def sync(input_path, output_path):
    input_storage = get_backend(input_path)
    output_storage = get_backend(output_path)

    if not isinstance(input_storage, LocalFileStorage) and not isinstance(output_storage, LocalFileStorage):
        raise ValueError('either input_path or output_path must be local file system')

    if input_path == output_path:
        return

    if Archive(input_path).valid and output_storage.is_dir():
        with TemporaryDirectory() as temp_dir:
            archive_path = os.path.join(temp_dir, os.path.basename(input_path))
            input_storage.sync_to(archive_path)
            Archive(archive_path).extract(output_path)
    elif Archive(output_path).valid and input_storage.is_dir():
        with TemporaryDirectory() as temp_dir:
            output_path = os.path.join(temp_dir, os.path.basename(input_path))
            Archive(output_path).create(input_path)
            output_storage.sync_from(input_path)
    else:
        input_storage.sync_to(output_path)
