import os
import tarfile
import zipfile
import shutil

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

from .utils import ChangeDirectory


class Archive(object):

    def __init__(self, path):
        self.path = path
        self.extract_handlers = {
            '.tar.gz': self._extract_targz,
            '.zip': self._extract_zip,
        }
        self.extension = self._extension(self.path)
        self.valid = self.extension in self.extract_handlers

    def extract(self, output_dir):
        handler = self.extract_handlers.get(self.extension)
        if handler is None:
            raise ValueError('unknown archive format in %s, unable to extract' % (self.path, ))
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        handler(output_dir)

    def create(self, input_path, format='zip'):
        extension = '.%s' % (format, )
        output_path = self.path
        if output_path.endswith(extension):
            output_path = output_path[:-1 * len(extension)]
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        shutil.make_archive(output_path, format, input_path)

    def _extract_targz(self, output_dir):
        tar = tarfile.open(self.path, 'r:gz')
        with ChangeDirectory(output_dir):
            tar.extractall()

    def _extract_zip(self, output_dir):
        with zipfile.ZipFile(self.path, 'r') as zip_file:
            zip_file.extractall(output_dir)

    def _extension(self, path):
        if '://' in path:
            path = urlparse(path).path
        if path.endswith('.tar.gz'):
            return '.tar.gz'
        return os.path.splitext(path)[1]
