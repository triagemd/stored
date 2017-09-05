import os
import tempfile
import base64


def with_backend_auth(func):
    def auth_and_call(*args, **kwargs):
        encoded_auth = os.environ.get('GCLOUD_ACCOUNT')
        if encoded_auth:
            with tempfile.NamedTemporaryFile() as auth_file:
                auth_file.write(base64.b64decode(encoded_auth))
                auth_file.flush()
                return func(*args, **kwargs)
        return func(*args, **kwargs)
    return auth_and_call
