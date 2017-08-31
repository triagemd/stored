import tarfile
import zipfile


from .utils import ChangeDirectory


class Archive(object):

    def __init__(self, file):
        self.file = file

    def extract(self, output_dir):
        if self.file.name.lower().endswith('.tar.gz'):
            self._extract_targz(self.file.name, output_dir)
        elif self.file.name.lower().endswith('.zip'):
            self._extract_zip(self.file.name, output_dir)
        else:
            raise ValueError('unknown archive format in %s, unable to extract' % (self.file.name, ))

    def _extract_targz(self, archive_file, output_dir):
        tar = tarfile.open(archive_file, 'r:gz')
        with ChangeDirectory(output_dir):
            tar.extractall()

    def _extract_zip(self, archive_file, output_dir):
        with zipfile.ZipFile(archive_file, 'r') as zip_file:
            zip_file.extractall(output_dir)
