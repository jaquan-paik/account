from copy import deepcopy
from datetime import date, datetime

from django.test import TestCase

from lib.utils.date import ceil_datetime_by_hour, floor_datetime_by_hour, get_month_start_end_date


class MonthStartEndDateTestCase(TestCase):
    def test_valid_date(self):
        years = [2017, 2018, 2019, 2020]
        months = range(1, 13)
        for year in years:
            for month in months:
                start_date, end_date = get_month_start_end_date(year, month)
                self.assertEqual(1, start_date.day)
                with self.assertRaises(ValueError):
                    date(year=year, month=month, day=end_date.day + 1)


class DatetimeFloorAndCeilTestCase(TestCase):
    def setUp(self):
        self.sample_dt = datetime(year=2018, month=1, day=11, hour=17, minute=13, second=15, microsecond=12)

    def test_valid_floor(self):
        dt = floor_datetime_by_hour(deepcopy(self.sample_dt))
        self.assertEqual(self.sample_dt.hour, dt.hour)
        self.assertEqual(0, dt.minute)
        self.assertEqual(0, dt.second)
        self.assertEqual(0, dt.microsecond)

    def test_valid_ceil(self):
        dt = ceil_datetime_by_hour(deepcopy(self.sample_dt))
        self.assertEqual(self.sample_dt.hour + 1, dt.hour)
        self.assertEqual(0, dt.minute)
        self.assertEqual(0, dt.second)
        self.assertEqual(0, dt.microsecond)
