from app.filters.BaseFilter import BaseFilter


class CleanSourceMapFilter(BaseFilter):
    def __init__(self):
        super().__init__()

        self.enforce = True
        self.input_extensions = ["js"]

    def apply(self, file_contents, filename):
        contents = file_contents.decode("utf8")
        # find the beginning of sourceMappingURL declaration
        sourcemap_start = contents.find("//# sourceMappingURL=")
        # skip if we can't find it
        if sourcemap_start != -1:
            # find the ending of the declaration
            sourcemap_end = contents.find(".map", sourcemap_start)
            # only take the css without the sourceMappingURL declaration
            contents = contents[0:sourcemap_start] + contents[sourcemap_end + 4:len(contents)]

        return contents
