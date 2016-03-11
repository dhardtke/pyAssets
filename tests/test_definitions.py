from unittest import TestCase

from mock import patch

from app.definitions import Definitions


class TestDefinitions(TestCase):
    def setUp(self):
        # create a basic Definitions object
        self.definitions = Definitions()

    def tearDown(self):
        self.definitions.clear()

    @patch("os.path", autospec=True)
    def test_get_dependencies_files(self, mock):
        self.definitions.add(name="b", files=["b.js"], dependencies=[], is_internal=False)
        self.definitions.add(name="a", files=["a.js"], dependencies=["b"], is_internal=False)

        self.assertEquals(["b.js"], self.definitions.get_dependencies_files(self.definitions["a"]["dependencies"]))

    def test_add(self):
        # non-existant file
        with self.assertRaises(FileNotFoundError):
            self.definitions.add(name="a", files=["invalid.js"])
        self.definitions.clear()

        # non-existant dependency
        with self.assertRaises(KeyError):
            self.definitions.add(name="a", dependencies=["b"])

        # duplicate definition
        with self.assertRaises(KeyError):
            self.definitions.add(name="a")

        # regular adding
        with patch("os.path", autospec=True) as mock:
            self.definitions.add(name="regular", files=["blub.js"])

            self.assertEquals({"files": ["blub.js"], "dependencies": [], "is_internal": False}, self.definitions["regular"])

    def test_clear(self):
        with patch("os.path", autospec=True) as mock:
            self.definitions.add(name="regular", files=["blub.js"])

        # ensure definition has been added
        self.assertGreater(len(self.definitions), 0)

        self.definitions.clear()
        # there should be 0 items left
        self.assertEquals(len(self.definitions), 0)