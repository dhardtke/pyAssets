from app.helpers import get_extension_from_filename


class BaseFilter:
    def __init__(self):
        # should this filter be active, regardless of enabled debug mode or file having been minified already?
        self.enforce = False
        # the extensions this filter is responsible for (i.e. js, or css, etc.)
        self.input_extensions = []

    def apply(self, file_contents, filename):
        # TODO implement check to check for binaries required to run this Filter
        raise NotImplementedError

    @staticmethod
    def get_output_extension(filename):
        file_ext = get_extension_from_filename(filename)
        # TODO refinement
        if file_ext == "js":
            return "js"
        else:
            return "css"

    @staticmethod
    def get_filters_for_file(filename, filters_enabled):
        from app.filters.Base64Filter import Base64Filter
        from app.filters.CleanCssFilter import CleanCssFilter
        from app.filters.CleanSourceMapFilter import CleanSourceMapFilter
        from app.filters.SassFilter import SassFilter
        from app.filters.UglifyJsFilter import UglifyJsFilter

        # the order of the filters is very important here
        included_filters = [SassFilter(), Base64Filter(), CleanCssFilter(), UglifyJsFilter(), CleanSourceMapFilter()]
        available_filters = list(filter(lambda _f: _f.__repr__() in filters_enabled, included_filters))
        filters = []
        ext = get_extension_from_filename(filename)

        for f in available_filters:
            if ext in f.input_extensions:
                filters.append(f)

        return filters

    def __repr__(self):
        return type(self).__name__
