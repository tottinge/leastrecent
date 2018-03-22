import unittest
from datetime import timedelta

from lib.dateparser import DateParser


class TestDateParser(unittest.TestCase):
    good_date = 'Mon Jan 1 01:23:33 2018 -1000'
    correct_offset = -timedelta(hours=10)

    def test_blank_is_not_a_MATCH(self):
        self.assertFalse(DateParser('').has_date())

    def test_date_is_detected(self):
        self.assertTrue(DateParser(self.good_date).has_date())

    def test_date_embedded_in_string(self):
        embedded = "prefix " + self.good_date + " suffix"
        self.assertTrue(DateParser(embedded).has_date())

    def test_parsing_nondate(self):
        d = DateParser("bullsnort")
        self.assertFalse(d.has_date())
        self.assertIsNone(d.date())

    def test_correct_date(self):
        d = DateParser(self.good_date).date()
        self.assertEqual(2018, d.year)
        self.assertEqual(1, d.month)
        self.assertEqual(1, d.day)
        self.assertEqual(0, d.weekday())
        self.assertEqual(self.correct_offset, d.utcoffset())

    def test_weird_date_problem_regression(self):
        weird_date = 'Tue Mar 20 16:59:05 2018 -0400'
        d = DateParser(weird_date).date()



    def test_prefix_doesnt_matter(self):
        prefixed = "prefix prefix " + self.good_date
        suffixed = self.good_date + "nonsense 1231 numbers 12312 -1999 stuff"
        wrapped = "Julie Shot A Bear " + self.good_date + " and hilarity ensued"

        expected = DateParser(self.good_date).date()
        self.assertEqual(expected, DateParser(prefixed).date())
        self.assertEqual(expected, DateParser(suffixed).date())
        self.assertEqual(expected, DateParser(wrapped).date())


