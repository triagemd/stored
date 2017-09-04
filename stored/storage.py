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

    def sync_to(self, output_path):
        if self.url == output_path:
            return
        if self._should_extract(output_path):
            with TemporaryDirectory() as temp_dir:
                archive_path = os.path.join(temp_dir, os.path.basename(self.url))
                self.backend.sync_to(archive_path)
                Archive(archive_path).extract(output_path)
        else:
            self.backend.sync_to(output_path)

    def sync_from(self, input_path):
        if self.url == input_path:
            return
        if self._should_archive(input_path):
            with TemporaryDirectory() as temp_dir:
                output_path = os.path.join(temp_dir, os.path.basename(self.url))
                Archive(output_path).create(input_path)
                self.backend.sync_from(output_path)
        else:
            self.backend.sync_from(input_path)

    def _should_extract(self, output_path):
        return Archive(self.url).valid and (os.path.isdir(output_path) or output_path.endswith('/'))

    def _should_archive(self, input_path):
        return (os.path.isdir(input_path) or input_path.endswith('/')) and Archive(self.url).valid
