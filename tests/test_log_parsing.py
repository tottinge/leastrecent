import unittest
from datetime import datetime, timezone, timedelta

from lib.dateparser import DateParser
from least_recent_change import least_recent_change


class LeastRecentChangeAlgorithm(unittest.TestCase):

    def test_single_commit(self):
        sample = """commit 2bca78243f97e96d6679e6a67abe505c899da875
Author: EMA\CZimmerman <czimmerman@emoneyadvisor.com>
Date:   Wed Mar 21 08:21:07 2018 -0400

    Hides Morningstar report modal when form is submitted.

11	1	advisor-site/ema/emx/ClientReports/Morningstar/Modal.js
1	0	advisor-site/ema/emx/MorningstarModal/constants.js
"""
        history = least_recent_change(sample.split('\n'))
        self.assertEqual(2, len(history), "Should be two files, but there are %d" % len(history))
        self.assertIn('advisor-site/ema/emx/ClientReports/Morningstar/Modal.js', history)
        self.assertIn('advisor-site/ema/emx/MorningstarModal/constants.js', history)
        expected = datetime(2018, 3, 21, 8, 21, 7, 0, timezone(-timedelta(hours=4)))
        self.assertTrue(all(v == expected for v in history.values()))

    def test_overriding_commits(self):
        sample = """    
Date: Sat Mar 17 12:00:00 2018 -0400
    * Earliest change - Mar 17 was saturday
3 3  Change/Charlie


Date: Wed Mar 21 08:21:00 2018 -0400
    * Latest Change - Wednesday of the same week
11 1  Change/Abel
1  1  Change/Baker
33 33  Change/Charlie

Date: Mon Mar 19 02:00:00 2018 -0400
   * Middle Change - Monday between saturday and wednesday
1 1 Change/Abel
2 2 Change/Baker
"""
        earlyDate = DateParser(" Sat Mar 17 12:00:00 2018 -0400").date()
        middleDate = DateParser("Mon Mar 19 02:00:00 2018 -0400").date()

        subject = least_recent_change(sample.split('\n'))
        self.assertEqual(subject['Change/Abel'], middleDate)
        self.assertEqual(subject['Change/Baker'], middleDate)
        self.assertEqual(subject['Change/Charlie'], earlyDate)