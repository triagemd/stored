import os
import requests
import shutil

from backports.tempfile import TemporaryDirectory
from google.cloud import storage

from .archive import Archive


class Storage(object):

    def __init__(self, url):
        self.url = url

    def list_files(self, relative=False):
        if '://' not in self.url:
            matches = []
            for root, dirnames, filenames in os.walk(self.url):
                for filename in filenames:
                    file_path = os.path.join(root, filename)
                    if relative:
                        file_path = os.path.relpath(file_path, self.url)
                    matches.append(file_path)
            return matches
        else:
            raise ValueError('Unknown storage URL scheme for %s' % (self.url, ))

    def download_and_extract(self, output_dir):
        with TemporaryDirectory() as temp_dir:
            archive_path = os.path.join(temp_dir, os.path.basename(self.url))
            with open(archive_path, 'wb') as archive_file:
                Storage(self.url).download_as_file(archive_file)
                Archive(archive_file).extract(output_dir)

    def download(self, output_path):
        with open(output_path, 'wb') as output_file:
            self.download_as_file(output_file)

    def download_as_file(self, output_file):
        url = self.url
        if url.startswith('gs://'):
            url = url.replace('gs://', '')
            bucket, path = url.split('/', 1)
            client = storage.Client()
            bucket = client.get_bucket(bucket)
            blob = bucket.get_blob(path)
            blob.download_to_file(output_file)
        elif url.startswith('http://') or url.startswith('https://'):
            response = requests.get(url, stream=True)
            if response.status_code == 200:
                for chunk in response:
                    output_file.write(chunk)
            else:
                raise ValueError(response)
        elif '://' not in url:
            shutil.copyfile(url, output_file.name)
        else:
            raise ValueError('Unknown storage URL scheme for %s' % (url, ))
        output_file.seek(0)

    def archive_and_upload(self, input_dir):
        with TemporaryDirectory() as temp_dir:
            archive_path = os.path.join(temp_dir, os.path.basename(self.url))
            with open(archive_path, 'wb') as archive_file:
                Archive(archive_file).create(input_dir)
                self.upload_from_file(archive_file)

    def upload_from_file(self, input_file):
        pass
