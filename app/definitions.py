import os

import yaml


class Definitions:
    def __init__(self):
        self.data = {}  # this will hold our definitions

    def __iter__(self):
        return self.data.__iter__()

    def __getitem__(self, item):
        return self.data.__getitem__(item)

    def __len__(self):
        return self.data.__len__()

    def load_from_file(self, filename, working_dir=None):
        if not os.path.isfile(filename):
            raise FileNotFoundError(filename)

        # switch working dir if necessary
        if working_dir is not None:
            os.chdir(working_dir)

        # ensure definitions are empty
        self.data = {}

        stream = open(filename, "r")
        bundles = yaml.load(stream)

        def add_bundle(name, files, dependencies, is_internal=False):
            self.data[name] = {
                "files": [] if files is None else files,
                "dependencies": [] if dependencies is None else dependencies,
                "is_internal": is_internal
            }

        # only take care of internal collections if they actually exist
        if "internals" in bundles:
            for bundle in bundles["internals"]:
                b = bundles["internals"][bundle]
                add_bundle(bundle, b["files"] if "files" in b else None,
                           b["dependencies"] if "dependencies" in b else None,
                           True)

            del bundles["internals"]

        for bundle in bundles:
            b = bundles[bundle]
            add_bundle(bundle, b["files"] if "files" in b else None, b["dependencies"] if "dependencies" in b else None)

        self.check_validity()

    def check_validity(self):
        """
            checks validity of current definitions
            :raises FileNotFoundError when a file in a bundle definition does not exist
            :raises KeyError when a dependency does not exist
        """
        for k in self.data:
            b = self.data[k]
            # check file existance
            for file in b["files"]:
                if not os.path.isfile(file):
                    raise FileNotFoundError(file)

            # check dependency correctness
            for dependency in b["dependencies"]:
                if dependency not in self.data:
                    raise KeyError(dependency)
