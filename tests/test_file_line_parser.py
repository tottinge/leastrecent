import unittest

from lib.filelineparser import FileLineParser


class FileLineParserTest(unittest.TestCase):
    def test_empty_line(self):
        self.assertIsNone(FileLineParser("").filename())

    def test_line_with_filename(self):
        sample = "10 102 /dont/eat/the/daisies.js"
        self.assertIsNotNone(FileLineParser(sample).filename())