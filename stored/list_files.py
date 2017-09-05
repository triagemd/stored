from .backends import get_backend


def list_files(path, relative=True):
    storage = get_backend(path)
    return storage.list(relative=relative)
