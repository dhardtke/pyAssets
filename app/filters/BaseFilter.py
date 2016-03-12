from app.helpers import get_extension_from_filename


class BaseFilter:
    def __init__(self):
        self.enforce = False  # should this filter be active, regardless of enabled debug mode or file having been minified already?
        self.input_extensions = []  # the extensions this filter is responsible for (i.e. js, or css, etc.)

    def apply(self, file_contents, filename):
        # TODO implement check to check for cleancss, somewhere in BaseFilter
        raise NotImplementedError

    @staticmethod
    def get_output_extension(filename):
        file_ext = get_extension_from_filename(filename)
        # TODO refinement
        if file_ext == "js":
            return "js"
        else:
            return "css"

    def __repr__(self):
        return type(self).__name__
