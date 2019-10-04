from datetime import datetime


class RFC3339:
    @staticmethod
    def to_obj(date):
        [date, microseconds] = date.split('.')
        date = (''.join(date)).split('T')
        days = date[0].split('-')
        time = date[1].split(':')
        microseconds = microseconds[:6]

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
