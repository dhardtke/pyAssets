import os

import yaml


class Definitions:
    def __init__(self):
        self.data = {}  # this will hold our definitions

    def __iter__(self):
        return self.data.__iter__()

    def __getitem__(self, item):
        return self.data.__getitem__(item)

    def add(self, name, files=None, dependencies=None, is_internal=False, check_validity=True):
        """
        add a new definition
        :param name: name of the definition
        :param files: a list of files or None
        :param dependencies: a list of dependencies or None
        :param is_internal: internal definitions won't get written to the filesystem
        """
        if dependencies is None:
            dependencies = []
        if files is None:
            files = []

        if name in self.data:
            raise KeyError("%s is already defined" % name)

        self.data[name] = {
            "files": files,
            "dependencies": dependencies,
            "is_internal": is_internal
        }

        if check_validity:
            # check validity of this definition
            self._check_validity(name)

    def clear(self):
        """
        clear all definitions
        """
        self.data = {}

    def __len__(self):
        return self.data.__len__()

    def load_from_file(self, filename, working_dir=None):
        """
        load the definitions from a given definitions file (yaml)
        :param filename: filename of the definitions file
        :param working_dir: working directory to use for reading files, or None
        """
        if not os.path.isfile(filename):
            raise FileNotFoundError(filename)

        if working_dir is not None:
            # switch working dir to supplied working_dir
            os.chdir(working_dir)
        else:
            # switch working dir to the dir where the definitions file resides
            os.chdir(os.path.dirname(os.path.abspath(filename)))

        # ensure definitions are empty
        self.clear()

        stream = open(filename, "r")
        bundles = yaml.load(stream)

        # only take care of internal collections if they actually exist
        if "internals" in bundles:
            for bundle in bundles["internals"]:
                b = bundles["internals"][bundle]
                self.add(bundle, b["files"] if "files" in b else [], b["dependencies"] if "dependencies" in b else [],
                         is_internal=True, check_validity=False)

            del bundles["internals"]

        for bundle in bundles:
            b = bundles[bundle]
            self.add(bundle, b["files"] if "files" in b else [], b["dependencies"] if "dependencies" in b else [],
                     is_internal=False, check_validity=False)

        # check validity later on
        for name in bundles:
            self._check_validity(name)

    def _check_validity(self, name):
        """
            checks validity one definition file
            :param name: name of the definition to check
            :raises FileNotFoundError when a file in a bundle definition does not exist
            :raises KeyError when a dependency does not exist
        """
        b = self.data[name]
        # check file existance
        for file in b["files"]:
            if not os.path.isfile(file):
                raise FileNotFoundError(file)

        # check dependency correctness
        for dependency in b["dependencies"]:
            if dependency not in self.data:
                raise KeyError("%s not known for definition of %s" % (dependency, name))

    def get_dependencies_files(self, dependencies):
        """
        get a list of all files for a given list of dependencies
        :param dependencies: the dependency list
        :return: list of files
        """
        files = []

        for name in dependencies:
            dependency = self.data[name]

            if "dependencies" in dependency:
                files.extend(self.get_dependencies_files(dependency["dependencies"]))

            if "files" in dependency:
                files.extend(dependency["files"])

        return files
