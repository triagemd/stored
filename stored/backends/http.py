import os
import requests

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse


class HTTPStorage(object):

    def __init__(self, url):
        self.url = url
        self.filename = os.path.basename(urlparse(url).path)

    def list(self, relative=False):
        raise NotImplementedError('list is not implemented for HTTPStorage backend')

    def sync_to(self, output_path):
        with open(output_path, 'wb') as output_file:
            response = requests.get(self.url, stream=True)
            if response.status_code == 200:
                for chunk in response:
                    output_file.write(chunk)
            else:
                raise ValueError(response)

    def sync_from(self, input_path):
        raise NotImplementedError('sync_from is not implemented for HTTPStorage backend')

    def is_dir(self):
        return False
