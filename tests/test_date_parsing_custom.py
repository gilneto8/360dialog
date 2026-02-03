import unittest
from datetime import datetime
from app.bot.parsers.utils import parse_smart_date


class TestDateParsing(unittest.TestCase):
    def setUp(self):
        self.base_date = datetime(2026, 3, 2, 11, 0)

    def test_full_format(self):
        res = parse_smart_date("2026-03-02 15:00", self.base_date)
        self.assertEqual(res, datetime(2026, 3, 2, 15, 0))

    def test_date_only(self):
        res = parse_smart_date("2026-03-05", self.base_date)
        self.assertEqual(res, datetime(2026, 3, 5, 11, 0))

    def test_mm_dd_hh_mm(self):
        res = parse_smart_date("03-02 15:00", self.base_date)
        self.assertEqual(res, datetime(2026, 3, 2, 15, 0))

        res = parse_smart_date("02-28 10:00", self.base_date)
        self.assertEqual(res, datetime(2027, 2, 28, 10, 0))

    def test_mm_dd(self):
        res = parse_smart_date("03-05", self.base_date)
        self.assertEqual(res, datetime(2026, 3, 5, 11, 0))

        res = parse_smart_date("02-28", self.base_date)
        self.assertEqual(res, datetime(2027, 2, 28, 11, 0))

    def test_dd_hh_mm(self):
        res = parse_smart_date("02 15:00", self.base_date)
        self.assertEqual(res, datetime(2026, 3, 2, 15, 0))

        res = parse_smart_date("01 10:00", self.base_date)
        self.assertEqual(res, datetime(2026, 4, 1, 10, 0))

    def test_dd_hh(self):
        res = parse_smart_date("02 15", self.base_date)
        self.assertEqual(res, datetime(2026, 3, 2, 15, 0))

        res = parse_smart_date("01 10", self.base_date)
        self.assertEqual(res, datetime(2026, 4, 1, 10, 0))

    def test_single_number_is_hour(self):
        res = parse_smart_date("02", self.base_date)
        self.assertEqual(res, datetime(2026, 3, 3, 2, 0))

        res = parse_smart_date("15", self.base_date)
        self.assertEqual(res, datetime(2026, 3, 2, 15, 0))

    def test_weekdays(self):
        res = parse_smart_date("Tuesday", self.base_date)
        self.assertEqual(res, datetime(2026, 3, 3, 11, 0))

        res = parse_smart_date("Tue 18", self.base_date)
        self.assertEqual(res, datetime(2026, 3, 3, 18, 0))

        res = parse_smart_date("Monday 18:00", self.base_date)
        self.assertEqual(res, datetime(2026, 3, 2, 18, 0))

        res = parse_smart_date("Monday 09:00", self.base_date)
        self.assertEqual(res, datetime(2026, 3, 9, 9, 0))

    def test_time_only(self):
        res = parse_smart_date("18:00", self.base_date)
        self.assertEqual(res, datetime(2026, 3, 2, 18, 0))

        res = parse_smart_date("09:00", self.base_date)
        self.assertEqual(res, datetime(2026, 3, 3, 9, 0))

    def test_hour_only_fallback(self):
        res = parse_smart_date("0", self.base_date)
        self.assertEqual(res, datetime(2026, 3, 3, 0, 0))
