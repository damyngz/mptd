from datetime import datetime, timezone
from re import sub

OFFSET_DISPLACEMENT = 9
DEFAULT_TZ = timezone.utc


def get_granularity(s):
    return {'S5': 5,
            'S10': 10,
            'S15': 15,
            'S30': 30,
            'M1': 60,
            'M2': 120,
            'M4': 240,
            'M5': 300,
            'M10': 600,
            'M15': 900,
            'M30': 1800,
            'H1': 3600,
            'H2': 7200,
            'H3': 10800,
            'H4': 14400,
            'H6': 21600,
            'H8': 28800,
            'H12': 43200,
            'D': 86400,
            'W': 604800,
            'M': 2678400}[s]


class RFC3339Error(Exception):
    def __init__(self, s):
        self.s = s

    def __str__(self):
        return self.s


class RFC3339:

    STANDARD_FMT_STRING = '%Y-%m-%dT%H:%M:%S.%fZ'

    @staticmethod
    def to_std(date, ignore_offset=None):
        return RFC3339.to_str(date, RFC3339.STANDARD_FMT_STRING, ignore_offset)

    @staticmethod
    def to_obj(date, ignore_offset=None, timezone=DEFAULT_TZ):
        if ignore_offset is not None and not isinstance(ignore_offset, bool):
            raise RFC3339Error('ignore_offset must be bool or None')

        try:
            [date, offset] = date.split('.')
            no_offset = False
        except ValueError:
            date = date.split('.')
            no_offset = True

        date = (''.join(date)).split('T')
        days = date[0].split('-')
        time = date[1].split(':')
        if not no_offset and not ignore_offset:
            offset = offset[:6]
        else:
            offset = 0

        return datetime(year=int(days[0]),
                        month=int(days[1]),
                        day=int(days[2]),
                        hour=int(time[0]),
                        minute=int(time[1]),
                        second=int(time[2]),
                        microsecond=int(offset),
                        tzinfo=timezone)

    @staticmethod
    def to_str(date, fmt_string, ignore_offset=None):
        """
        :param ignore_offset: defaults to False
        :param date: accepts str or datetime object
        :param fmt_string:
        :return:
        """
        dt_string, ind = '', -1
        # if %f in fmt_string, calculate offset and add into string
        if fmt_string.find('%f') != -1:
            ind = fmt_string.find('%f')
            fmt_string = sub('%f', '%f000', fmt_string)

        if isinstance(date, str):
            dt = RFC3339.to_obj(date, ignore_offset=ignore_offset)
        # does not check for error
        # TODO catch argument error?
        else:
            dt = date
        if ignore_offset:
            dt = dt.replace(microsecond=0)

        # print(dt)
        dt_string = dt.strftime(fmt_string)
        return dt_string



