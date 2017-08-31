import os

from backports.tempfile import TemporaryDirectory

from .archive import Archive
from .backends import get_backend


class Storage(object):

    def __init__(self, url):
        self.url = url
        self.backend = get_backend(url)

    def list(self, relative=False):
        return self.backend.list(relative=relative)

    def download(self, output_path, extract=False):
        if extract:
            with TemporaryDirectory() as temp_dir:
                archive_path = os.path.join(temp_dir, os.path.basename(self.url))
                self.backend.download(archive_path)
                Archive(archive_path).extract(output_path)
        else:
            self.backend.download(output_path)

    def upload(self, input_path, archive=False):
        if archive:
            with TemporaryDirectory() as temp_dir:
                output_path = os.path.join(temp_dir, os.path.basename(self.url))
                Archive(output_path).create(input_path)
                self.backend.upload(output_path)
        else:
            self.backend.upload(input_path)
