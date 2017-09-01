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

    def download(self, output_path):
        output_dir = os.path.dirname(output_path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        shutil.copyfile(self.path, output_path)

    def upload(self, input_path):
        output_dir = os.path.dirname(self.path)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        shutil.copyfile(input_path, self.path)
