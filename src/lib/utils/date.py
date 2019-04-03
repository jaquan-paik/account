import calendar
from datetime import date, datetime, timedelta
from time import mktime, time
from typing import Tuple

import pytz
from dateutil import parser
from django.utils.http import http_date

from lib.utils.format import DateTimeFormat


def get_month_start_end_date(year: int, month: int) -> Tuple:
    monthrange = calendar.monthrange(year, month)
    start_date = date(year=year, month=month, day=1)
    end_date = date(year=year, month=month, day=monthrange[1])
    return start_date, end_date


def strptime(datetime_string: str, datetime_format=DateTimeFormat.YMD_HMSM) -> datetime:
    return datetime.strptime(datetime_string, datetime_format)


def reset_minutes(_datetime: datetime) -> datetime:
    return _datetime.replace(minute=0, second=0, microsecond=0)


def floor_datetime_by_hour(_datetime: datetime) -> datetime:
    return reset_minutes(_datetime)


def ceil_datetime_by_hour(_datetime: datetime) -> datetime:
    return floor_datetime_by_hour(_datetime) + timedelta(hours=1)


def to_unix_time_seconds(_datetime: datetime) -> int:
    return int(mktime(_datetime.timetuple()))


def to_http_date(_datetime: datetime) -> str:
    return http_date(to_unix_time_seconds(_datetime))


def get_timedelta_seconds(next_minute: int) -> int:
    """
    get_timedelta_seconds(60) -> 매 시간단위로 다음 시간까지 남은 시간을 구함
    get_timedelta_seconds(10) -> 10분 단위로 다음 시간까지 남은 시간을 구함 (10분, 20분, ...)
    get_timedelta_seconds(5) -> 5분 단위로 다음 시간까지 남은 시간을 구함 (5분, 10분, 15분, ...)
    """
    now = datetime.now()
    minute_delta = next_minute - (now.minute % next_minute)
    next_time = now.replace(second=0, microsecond=0) + timedelta(minutes=minute_delta)
    return int((next_time - now).total_seconds())


def convert_minute_to_seconds(minute: int) -> int:
    return int(timedelta(minutes=minute).total_seconds())


def date_range(start_date: date, end_date: date) -> date:
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)


def convert_2digit_year_to_4digit(two_digit_year: int) -> int:
    current_year_2digit = int(str(datetime.now().year)[2:])
    if two_digit_year > current_year_2digit:
        return 1900 + two_digit_year
    return 2000 + two_digit_year


def diff_month(d1, d2) -> int:
    return (d1.year - d2.year) * 12 + d1.month - d2.month


def get_first_day() -> datetime:
    return parser.parse('1970-01-01T09:00:00')


def get_last_day() -> datetime:
    return parser.parse('9999-12-31T23:59:59')


def make_tz_aware(dt_unaware: datetime) -> datetime:
    if dt_unaware is None:
        return None

    # 싱글턴인데 UTC를 자꾸 pylint가 잡아서 예외처리
    return pytz.UTC.localize(dt_unaware - timedelta(hours=9))  # pylint: disable=no-value-for-parameter


def get_current_timestamp() -> int:
    return int(round(time() * 1000))


def generate_cookie_expire_time(expires_in: int, target_datetime: datetime):
    return datetime.strftime(target_datetime.utcnow() + timedelta(seconds=expires_in), DateTimeFormat.COOKIE)
