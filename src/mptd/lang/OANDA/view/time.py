from datetime import datetime


class RFC3339:

    STANDARD_FMT_STRING = '%Y-%m-%dT%H:%M:%S.%f000Z'

    @staticmethod
    def to_std(date):
        return RFC3339.to_str(date, RFC3339.STANDARD_FMT_STRING)

    @staticmethod
    def to_obj(date):
        try:
            [date, microseconds] = date.split('.')
            no_microseconds = False
        except ValueError:
            date = date.split('.')
            no_microseconds = True

        date = (''.join(date)).split('T')
        days = date[0].split('-')
        time = date[1].split(':')
        if not no_microseconds:
            microseconds = microseconds[:6]
        else:
            microseconds = 0

        return datetime(year=int(days[0]),
                        month=int(days[1]),
                        day=int(days[2]),
                        hour=int(time[0]),
                        minute=int(time[1]),
                        second=int(time[2]),
                        microsecond=int(microseconds))

    @staticmethod
    def to_str(date, fmt_string):
        """
        :param date: accepts str or datetime object
        :param fmt_string:
        :return:
        """
        if isinstance(date, str):
            dt = RFC3339.to_obj(date)

        # does not check for error
        # TODO catch argument error?
        else:
            dt = date
        return dt.strftime(fmt_string)
