from unittest import TestCase

from app.filters.Base64Filter import Base64Filter
from app.filters.BaseFilter import BaseFilter
from app.filters.CleanCssFilter import CleanCssFilter
from app.filters.CleanSourceMapFilter import CleanSourceMapFilter
from app.filters.SassFilter import SassFilter
from app.filters.UglifyJsFilter import UglifyJsFilter


# helper to turn a list of objects into a list of strings of their __repr__ results
def helper_get_repr_list(objects_list):
    return list(map(lambda o: o.__repr__(), objects_list))


class TestBaseFilter(TestCase):
    def test_get_output_extension(self):
        self.assertEquals("js", BaseFilter.get_output_extension("bundlename.js"))
        self.assertEquals("css", BaseFilter.get_output_extension("bundlename.css"))
        self.assertEquals("css", BaseFilter.get_output_extension("bundlename.scss"))
        self.assertEquals("css", BaseFilter.get_output_extension("bundlename.sass"))

    def test_get_filters_for_file(self):
        self.assertEquals([], BaseFilter.get_filters_for_file("filename.js", []))
        self.assertEquals(helper_get_repr_list([UglifyJsFilter(), CleanSourceMapFilter()]), helper_get_repr_list(
            BaseFilter.get_filters_for_file("filename.js",
                                            ["Base64Filter", "CleanCssFilter", "CleanSourceMapFilter", "SassFilter",
                                             "UglifyJsFilter"])))
        self.assertEquals(helper_get_repr_list([Base64Filter(), CleanCssFilter()]),
                          helper_get_repr_list(BaseFilter.get_filters_for_file("filename.css",
                                                                               ["Base64Filter",
                                                                                "CleanCssFilter",
                                                                                "CleanSourceMapFilter",
                                                                                "SassFilter",
                                                                                "UglifyJsFilter"])))
        self.assertEquals(helper_get_repr_list([SassFilter(), Base64Filter(), CleanCssFilter()]),
                          helper_get_repr_list(BaseFilter.get_filters_for_file("filename.sass",
                                                                               ["Base64Filter",
                                                                                "CleanCssFilter",
                                                                                "CleanSourceMapFilter",
                                                                                "SassFilter",
                                                                                "UglifyJsFilter"])))
