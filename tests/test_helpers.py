from unittest import TestCase

from app.helpers import filter_by_extensions


class TestHelpers(TestCase):
    def test_filter_by_extensions(self):
        self.assertEquals(["a.js", "b.js"], filter_by_extensions(["a", "b.exe", "a.js", "b.js.a", "b.js"], ["js"]))
        # TODO
