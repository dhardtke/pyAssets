from unittest import TestCase

from app.helpers import get_extension_from_filename


class TestHelpers(TestCase):
    def test_get_extension_from_filename(self):
        self.assertEquals("exe", get_extension_from_filename("c:\\file.exe"))
        self.assertEquals("", get_extension_from_filename(""))
        self.assertEquals("", get_extension_from_filename("a"))
        self.assertEquals("", get_extension_from_filename("\\|||"))
