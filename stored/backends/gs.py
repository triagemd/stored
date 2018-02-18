import os
import tempfile
import base64

from contextlib import contextmanager
from google.cloud import storage

from .local import LocalFileStorage


@contextmanager
def authed_client():
    encoded_auth = os.environ.get('GCLOUD_ACCOUNT')
    with tempfile.NamedTemporaryFile() as auth_file:
        auth_file.write(base64.b64decode(encoded_auth))
        auth_file.flush()
        os.fsync(auth_file.fileno())
        yield storage.Client.from_service_account_json(auth_file.name)


class GoogleStorage(object):

    def __init__(self, url):
        self.url = url
        url = url.replace('gs://', '')
        if '/' in url:
            self.bucket, self.path = url.split('/', 1)
        else:
            self.bucket = url
            self.path = ''
        self.filename = os.path.basename(self.path)

    def list(self, relative=False):
        with authed_client() as client:
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
            output_dir = os.path.dirname(output_path)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            with open(output_path, 'wb') as output_file:
                with authed_client() as client:
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
            with authed_client() as client:
                bucket = client.bucket(self.bucket)
                blob = bucket.blob(self.path)
                blob.upload_from_filename(filename=input_path)

    def is_dir(self, path=None):
        path = path or self.url
        _, extension = os.path.splitext(path)
        return len(extension) == 0 or path.endswith('/')
