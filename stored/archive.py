import tarfile
import zipfile

from .utils import ChangeDirectory


class Archive(object):

    def __init__(self, path):
        self.path = path

    def extract(self, output_dir):
        if self.path.lower().endswith('.tar.gz'):
            self._extract_targz(output_dir)
        elif self.path.lower().endswith('.zip'):
            self._extract_zip(output_dir)
        else:
            raise ValueError('unknown archive format in %s, unable to extract' % (self.path, ))

    def _extract_targz(self, output_dir):
        tar = tarfile.open(self.path, 'r:gz')
        with ChangeDirectory(output_dir):
            tar.extractall()

    def _extract_zip(self, output_dir):
        with zipfile.ZipFile(self.path, 'r') as zip_file:
            zip_file.extractall(output_dir)
