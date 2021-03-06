import os
import shutil
import subprocess
import tempfile

from app.filters.BaseFilter import BaseFilter
from app.helpers import get_extension_from_filename


class SassFilter(BaseFilter):
    def __init__(self):
        super().__init__()

        self.enforce = True
        self.input_extensions = ["scss", "sass"]

    def apply(self, file_contents, filename):
        # print("[SassFilter] Filtering %s\n" % filename)

        # use sassc when available
        if shutil.which("sassc") is not None:
            binary = "sassc"
        else:
            binary = "sass"

        args = [binary, "--load-path", os.path.dirname(os.path.abspath(filename)), "--cache-location",
                os.path.join(tempfile.gettempdir(), "sass-cache")]

        # only append "--scss" when using sass as compiler
        ext = get_extension_from_filename(filename)
        if ext == "scss" and binary == "sass":
            args.extend(["--scss"])

        args.extend(["--stdin"])

        process = subprocess.run(args, input=file_contents, env=os.environ, shell=True, stderr=subprocess.PIPE,
                                 stdout=subprocess.PIPE)

        if process.returncode != 0:
            last_lines = process.stderr.decode("utf8")
            raise ChildProcessError(
                "%s exited with error code %d, last lines of output:\n%s" % (binary, process.returncode, last_lines))

        return process.stdout.decode("utf8")
