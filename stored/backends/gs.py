import os

from google.cloud import storage


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
        client = storage.Client()
        bucket = client.bucket(self.bucket)
        blobs = bucket.list_blobs(prefix=self.path)
        for blob in blobs:
            if relative:
                yield blob.name
            else:
                yield os.path.join(self.url, blob.name)

    def download(self, output_path):
        with open(output_path, 'wb') as output_file:
            client = storage.Client()
            bucket = client.bucket(self.bucket)
            blob = bucket.blob(self.path)
            blob.download_to_file(output_file)

    def upload(self, input_path):
        client = storage.Client()
        bucket = client.bucket(self.bucket)
        blob = bucket.blob(self.path)
        blob.upload_from_filename(filename=input_path)
