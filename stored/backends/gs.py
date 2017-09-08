import os
import base64

from backports.tempfile import TemporaryDirectory
from contextlib import contextmanager
from google.cloud import storage

from .local import LocalFileStorage


@contextmanager
def auth():
    auth_file_path = os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')
    if auth_file_path and os.path.exists(auth_file_path):
        yield
        return
    encoded_auth = os.environ.get('GCLOUD_ACCOUNT')
    if encoded_auth:
        with TemporaryDirectory() as temp_dir:
            auth_file_path = os.path.join(temp_dir, 'auth.json')
            with open(auth_file_path, 'w') as auth_file:
                auth_file.write(base64.b64decode(encoded_auth).decode())
            os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = auth_file_path
            yield
    else:
        yield


class GoogleStorage(object):

    def __init__(self, url):
        self.url = url
        url = url.replace('gs://', '')
        if '/' in url:
            self.bucket, self.path = url.split('/', 1)
        else:
            self.bucket = url
            self.path = ''

    def list(self, relative=False):
        with auth():
            client = storage.Client()
            bucket = client.bucket(self.bucket)
            blobs = bucket.list_blobs(prefix=self.path)
            for blob in blobs:
                if relative:
                    yield blob.name
                else:
                    yield os.path.join(self.url, blob.name)

    def sync_to(self, output_path):
        if self.is_dir():
            output_paths = LocalFileStorage(output_path).list(relative=True)
            new_paths = set(self.list(relative=True)) - set(output_paths)
            for path in new_paths:
                GoogleStorage(os.path.join(self.url, path)).sync_to(os.path.join(output_path, path))
        else:
            with open(output_path, 'wb') as output_file:
                with auth():
                    client = storage.Client()
                    bucket = client.bucket(self.bucket)
                    blob = bucket.blob(self.path)
                    blob.download_to_file(output_file)

    def sync_from(self, input_path):
        if self.is_dir(input_path):
            input_paths = LocalFileStorage(input_path).list(relative=True)
            new_paths = set(input_paths) - set(self.list(relative=True))
            for path in new_paths:
                GoogleStorage(os.path.join(self.url, path)).sync_from(os.path.join(input_path, path))
        else:
            with auth():
                client = storage.Client()
                bucket = client.bucket(self.bucket)
                blob = bucket.blob(self.path)
                blob.upload_from_filename(filename=input_path)

    def is_dir(self, path=None):
        path = path or self.url
        _, extension = os.path.splitext(path)
        return len(extension) == 0 or path.endswith('/')
