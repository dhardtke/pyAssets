import os
import subprocess

from app.filters.BaseFilter import BaseFilter


class CleanCssFilter(BaseFilter):
    def __init__(self):
        super().__init__()

        self.input_extensions = ["css", "scss", "sass"]

    def apply(self, file_contents, filename):
        # print("[CleanCss] Filtering %s\n" % filename)

        # TODO implement check to check for cleancss, somewhere in BaseFilter
        process = subprocess.run(["cleancss", "--s0", "--skip-rebase"], input=file_contents, env=os.environ, shell=True,
                                 stderr=subprocess.PIPE, stdout=subprocess.PIPE)

        if process.returncode != 0:
            print(file_contents)
            last_lines = process.stderr.decode("utf8")
            raise ChildProcessError(
                "CleanCSS exited with error code %d, filename: %s, last lines of output:\n%s" % (
                    process.returncode, filename, last_lines))

        return process.stdout.decode("utf8")
