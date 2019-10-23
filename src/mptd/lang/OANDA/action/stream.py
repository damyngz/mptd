#!/usr/bin/env python3

import os, time, platform, csv
from v20.instrument import Candlestick
from datetime import datetime
from ..view.time import RFC3339

"""
Value	Description
S5	5 second candlesticks, minute alignment
S10	10 second candlesticks, minute alignment
S15	15 second candlesticks, minute alignment
S30	30 second candlesticks, minute alignment
M1	1 minute candlesticks, minute alignment
M2	2 minute candlesticks, hour alignment
M4	4 minute candlesticks, hour alignment
M5	5 minute candlesticks, hour alignment
M10	10 minute candlesticks, hour alignment
M15	15 minute candlesticks, hour alignment
M30	30 minute candlesticks, hour alignment
H1	1 hour candlesticks, hour alignment
H2	2 hour candlesticks, day alignment
H3	3 hour candlesticks, day alignment
H4	4 hour candlesticks, day alignment
H6	6 hour candlesticks, day alignment
H8	8 hour candlesticks, day alignment
H12	12 hour candlesticks, day alignment
D	1 day candlesticks, day alignment
W	1 week candlesticks, aligned to start of week
M	1 month candlesticks, aligned to first day of the month
"""

DEFAULT_POLL_RATE = 1
DEFAULT_PATH_DIRECTORY_WINDOWS = R'C:\Users\$USERNAME'
DEFAULT_PATH_DIRECTORY_LINUX = R'~/logs/'
DEFAULT_PATH_DIRECTORY = ''

# TODO implement logger objects
# TODO set proper default paths


def get_os_path_directory():
    global DEFAULT_PATH_DIRECTORY
    if platform.system().lower() == 'windows':
        DEFAULT_PATH_DIRECTORY = DEFAULT_PATH_DIRECTORY_WINDOWS
    elif platform.system().lower() == 'linux':
        DEFAULT_PATH_DIRECTORY = DEFAULT_PATH_DIRECTORY_LINUX


get_os_path_directory()


# -----------------------------------------------------------------------------------


def get_log_file_path(instrument,
                      granularity,
                      time_start,
                      time_end,
                      path_directory=DEFAULT_PATH_DIRECTORY,
                      num_ticks=None,
                      file_type='csv'):
    if num_ticks is None:
        num_ticks = ''
    file_name = '{0}_{1}_{2}_{3}_{4}'.format(instrument, granularity, num_ticks, time_start, time_end)
    file_name = ''.join([file_name, ".{}".format(file_type)])
    path = os.path.join(os.path.expanduser(path_directory), file_name)
    return path


def init_log_file(log_file_path):
    if os.path.isfile(log_file_path):
        return False
    else:
        with open(log_file_path, 'w') as file:
            file.write('')
        return True


def to_dict(candle):
    # time.split('.') removes microseconds, which are similar in poll
    return {'date_time': candle.time.split('.')[0],
            'open': candle.mid.o,
            'low': candle.mid.l,
            'high': candle.mid.h,
            'close': candle.mid.c,
            'volume': candle.volume}


def to_list(candle, list_params):
    return [candle[p] for p in list_params]


def get_tick(candle, g):
    """

    :param candle: Candle object
    :param g: (string) granularity
    :return: (dict) id value for candle for appending to sql query
    """
    # TODO check validity of g? (granularity)
    def _seconds(dt_obj):
        return dt_obj.second + (60 * dt_obj.minute) + (3600 * dt_obj.hour)

    def _days(dt_obj):
        return dt_obj.timetuple().tm_yday

    def _weeks(dt_obj):
        return dt_obj.isocalendar()[1]

    # 86400 seconds in a day, pre-calculated to reduce load
    ticks = 86400
    g_dict = {"S": 1,
              "M": 60,
              "H": 3600,
              "D": 1,
              "W": 1}

    # value declared to reduce calculations
    # len of ticks
    max_ticks = {'S5': 17280,
                 'S10': 8640,
                 'S15': 5760,
                 'S30': 2880,
                 'M1': 1440,
                 'M2': 720,
                 'M4': 360,
                 'M5': 288,
                 'M10': 144,
                 'M15': 96,
                 'M30': 48,
                 'H1': 24,
                 'H2': 12,
                 'H3': 8,
                 'H4': 6,
                 'H6': 4,
                 'H8': 3,
                 'H12': 2,
                 'D': 366,
                 'W': 52}

    degree = g_dict[g[0].upper()]
    magnitude = int(g[1:]) if len(g) > 1 else 1
    if isinstance(candle, Candlestick):
        candle_o = RFC3339.to_obj(candle.time)
    elif isinstance(candle, datetime):
        candle_o = candle
    else:
        raise InvalidTickError("Improper 'candle' argument passed. Must be Candle or datetime ")

    if g not in ['D', 'W']:
        s = _seconds(candle_o) // (degree * magnitude)
        fmt_str = '%Y%m%d'
    else:
        if g == 'D':
            s = _days(candle_o)
            fmt_str = '%Y'
        else:
            s = _weeks(candle_o)
            fmt_str = '%Y'

    # TODO implement check if calculation is exact (should produce float x.0, no dec places)

    # ensure ticks does not overflow max_ticks
    if s > max_ticks[g]:
        raise InvalidTickError('{ticks} > maximum of {max_ticks} for granularity = {granularity}'.format(
            ticks=s,
            max_ticks=max_ticks[g],
            granularity=g
        ))
    tick = RFC3339.to_str(candle_o, '%Y%m%d') + str(s).zfill(len(str(max_ticks[g])))
    return {'tick': tick}


class InvalidTickError:
    def __init__(self, s):
        self.s = s

    def __str__(self):
        return self.s


class FileHandler:
    def __init__(self,
                 path,
                 instrument,
                 granularity=None,
                 candles_per_file=100,
                 datetime_formatter='RFC3339',
                 logger=None):

        if granularity is None:
            self.granularity = "S5"
        else:
            self.granularity = granularity

        self.instrument = instrument
        self.path = path
        self.candles = None
        self.candles_per_file = candles_per_file
        self.datetime_formatter = datetime_formatter
        self.logger = logger

    def format_time(self, date):
        if self.datetime_formatter == 'RFC3339':
            s = RFC3339.to_str(date=date, fmt_string="%d%m%Y%H%M%S")

        elif self.datetime_formatter == 'unix':
            raise NotImplementedError

        return s

    def update(self, candles):
        if self.candles is None:
            self.candles = candles
            return

        print(len(self.candles))
        for candle in candles:
            if candle.complete and (candle.time > self.candles[-1].time):
                self.candles.append(candle)

                if self.logger:
                    self.logger.info(to_dict(candle))

        while len(self.candles) > self.candles_per_file:
            filename = get_log_file_path(instrument=self.instrument,
                                         granularity=self.granularity,
                                         time_start=self.format_time(self.candles[0].time),
                                         time_end=self.format_time(self.candles[-1].time),
                                         num_ticks=self.candles_per_file)

            # TODO change to logging
            print('writing to {}'.format(filename))
            with open(filename, 'w') as file:
                writer = csv.DictWriter(file, fieldnames=list(to_dict(candles[0])))

                writer.writeheader()
                # TODO write logging info for new file written
                for i in range(self.candles_per_file):
                    writer.writerow(to_dict(self.candles.pop(0)))


class CandleHolder:
    """
    holds candles and manages candle yielding
    """

    def __init__(self,
                 num_candles=20,
                 add_args=None,
                 add_ticks=False,
                 granularity=None
                 ):
        self.candles = []
        self.size = num_candles
        self.candle_formatter = ['time', 'open', 'high', 'low', 'close', 'volume']
        self.add_ticks = add_ticks
        if add_args and isinstance(add_args, dict):
            self.add_args = add_args
        else:
            self.add_args = {}

        # in inconsistent declarations, granularity declared in add_args take precedence
        if granularity is not None:
            self.granularity = granularity

        if 'granularity' in self.add_args:
            self.granularity = self.add_args['granularity']

            if granularity is not None and granularity != self.add_args['granularity']:
                # TODO raise warning/error inconsistent declaration of granularity
                pass

    def pop_candle(self, candles, pop_format='dict'):
        # TODO implement pop_format list or dict
        to_pop = []
        candles = candles[-(self.size+5):]

        if not self.candles:
            self.candles = [candles[0]]

        for candle in candles:
            if candle.complete and (RFC3339.to_obj(candle.time) > RFC3339.to_obj(self.candles[-1].time)):
                to_pop.append(candle)
                self.candles.pop(0)
                self.candles.append(candle)

        if to_pop:
            if self.add_ticks:
                return [{**to_dict(c), **self.add_args, **get_tick(c, self.granularity)} for c in to_pop]
            else:
                return [{**to_dict(c), **self.add_args} for c in to_pop]
            # candle_dicts = [to_dict(c) for c in to_pop]
            # return [to_list(c, self.candle_formatter) for c in candle_dicts]

        return []


# -----------------------------------------------------------------------------------
def instrument_candle_request(api,
                              instrument,
                              granularity=None,
                              count=500,
                              add_args=None
                              ):
    if add_args is None:
        add_args = {}
    kwargs = {'granularity': granularity,
              'count': count,
              **add_args}

    print(kwargs)
    response = api.context.instrument.candles(instrument, **kwargs)
    candles = response.get('candles', 200)
    return candles


def instrument_candle_poll(api,
                           instrument,
                           granularity=None,
                           logger=None,
                           poll_rate=DEFAULT_POLL_RATE,
                           write_to_file=False,
                           tick_label=False
                           ):
    if write_to_file:
        fh = FileHandler(path=DEFAULT_PATH_DIRECTORY,
                         instrument=instrument,
                         granularity=granularity,
                         datetime_formatter=api.datetime_format,
                         logger=logger)
    ch = CandleHolder(add_args={'instrument': instrument,
                                'granularity': granularity},
                      add_ticks=tick_label)
    while True:
        kwargs = {'granularity': granularity}

        response = api.context.instrument.candles(instrument, **kwargs)
        candles = response.get('candles', 200)

        # yield date_time, open, high, low, close, volume
        yield ch.pop_candle(candles)

        if write_to_file:
            fh.update(candles)
        time.sleep(poll_rate)


def instrument_pricing_stream(api,
                              instruments,
                              show_heartbeats=False,
                              snapshot=False,
                              include_time=False,
                              time_fmt=None):
    """
    :param api: v20 context
    :param instruments: fx instrument
    :param show_heartbeats: (bool) (Default=False)
    :param snapshot: (bool) (Default=False)
    :param include_time: (bool) bool to define whether a time string is returned(Default=False)
    :param time_fmt: strftime() string to format returned datetime string (str)
    :return: (list) containing relevant responses
    """

    # TODO implement logging?
    try:
        if isinstance(instruments, list):
            instruments_arg = ",".join(instruments)

        elif not (isinstance(instruments, str)):
            raise ValueError("\'{}\' type is not allowed.".format(type(instruments).__name__))

        else:
            instruments_arg = instruments

    except ValueError as e:
        print(e)

    response = api.streaming_context.pricing.stream(api.active_account,
                                                    snapshot=snapshot,
                                                    instruments=instruments_arg)

    # code duplication to reduce possible latency
    #
    if not include_time:
        for m_type, m in response.parts():
            if m_type == "pricing.ClientPrice":
                yield [m.instrument, m.bids[0].price, m.asks[0].price]

            elif m_type == "pricing.PricingHeartbeat":
                if show_heartbeats:
                    # TODO not implemented
                    pass
                pass

    else:
        # defines default time string format if not defined
        if time_fmt is None:
            time_fmt = "%Y/%m/%d-%H:%M:%S.%f"
            # t = RFC3339.to_str(m.time, "%H:%M:%S.%f")

        for m_type, m in response.parts():
            if m_type == "pricing.ClientPrice":
                t = RFC3339.to_str(m.time, time_fmt)
                yield [m.instrument, m.bids[0].price, m.asks[0].price, t]

            elif m_type == "pricing.PricingHeartbeat":
                if show_heartbeats:
                    # TODO not implemented
                    raise NotImplementedError
                pass
