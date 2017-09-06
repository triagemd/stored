import os
import shutil


class LocalFileStorage(object):

    def __init__(self, path):
        self.path = path

    def list(self, relative=False):
        matches = []
        for root, dirnames, filenames in os.walk(self.path):
            for filename in filenames:
                file_path = os.path.join(root, filename)
                if relative:
                    file_path = os.path.relpath(file_path, self.path)
                matches.append(file_path)
        return matches

    def sync_to(self, output_path):
        if not os.path.exists(self.path):
            return
        if self.is_dir(self.path):
            input_paths = self.list(relative=True)
            if not os.path.exists(output_path):
                os.makedirs(output_path)
            output_paths = LocalFileStorage(output_path).list(relative=True)
            new_paths = set(input_paths) - set(output_paths)
            for path in new_paths:
                LocalFileStorage(os.path.join(self.path, path)).sync_to(os.path.join(output_path, path))
        else:
            output_dir = os.path.dirname(output_path)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            shutil.copyfile(self.path, output_path)

    def sync_from(self, input_path):
        if not os.path.exists(input_path):
            return
        if self.is_dir(input_path):
            input_paths = LocalFileStorage(input_path).list(relative=True)
            if not os.path.exists(self.path):
                os.makedirs(self.path)
            output_paths = self.list(relative=True)
            new_paths = set(input_paths) - set(output_paths)
            for path in new_paths:
                LocalFileStorage(os.path.join(self.path, path)).sync_from(os.path.join(input_path, path))
        else:
            output_dir = os.path.dirname(self.path)
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            shutil.copyfile(input_path, self.path)

    def is_dir(self, path=None):
        if path is None:
            path = self.path
        _, extension = os.path.splitext(path)
        return os.path.isdir(path) or len(extension) == 0 or path.endswith('/')
