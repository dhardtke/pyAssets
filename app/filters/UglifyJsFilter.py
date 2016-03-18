import os
import subprocess

from app.filters.BaseFilter import BaseFilter


class UglifyJsFilter(BaseFilter):
    def __init__(self):
        super().__init__()

        self.input_extensions = ["js"]

    def apply(self, file_contents, filename):
        # print("[UglifyJS] Filtering %s" % files)
        process = subprocess.run(["uglifyjs", "-", "-c", "-m", "--screw-ie8", "--no-copyright"], input=file_contents,
                                 env=os.environ, shell=True, stderr=subprocess.PIPE, stdout=subprocess.PIPE)

        if process.returncode != 0:
            last_lines = process.stderr.decode("utf8")
            raise ChildProcessError(
                "UglifyJs exited with error code %d, last lines of output:\n%s" % (process.returncode, last_lines))

        return process.stdout.decode("utf8")
