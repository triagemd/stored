from .auth import with_backend_auth
from .backends import get_backend


@with_backend_auth
def list_files(path, relative=True):
    storage = get_backend(path)
    return storage.list(relative=relative)
