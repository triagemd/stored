from .local import LocalFileStorage
from .http import HTTPStorage
from .gs import GoogleStorage


def get_backend(url):
    if url.startswith('gs://'):
        return GoogleStorage(url)
    elif url.startswith('http://') or url.startswith('https://'):
        return HTTPStorage(url)
    elif '://' not in url:
        return LocalFileStorage(url)
    else:
        raise ValueError('Unknown storage URL scheme for %s' % (url, ))
