import curses


class CandlePrinter:

    def __init__(self, stdscr):
        self.stdscr = stdscr

        self.stdscr.clear()
        (h, w) = self.stdscr.getmaxyx()
        self.height = h
        self.width = w

        self.field_width = {
            'time': 19,
            'price': 8,
            'volume': 6,
        }

    def set_instrument(self, instrument):
        self.instrument = instrument

    def set_granularity(self, granularity):
        self.granularity = granularity

    def set_candles(self, candles):
        self.candles = candles

    def update_candles(self, candles):
        new = candles[0]
        last = self.candles[-1]

        # Candles haven't changed
        if new.time == last.time and new.volume == last.time:
            return False

        # Update last candle
        self.candles[-1] = candles.pop(0)

        # Add the newer candles
        self.candles.extend(candles)

        # Get rid of the oldest candles
        self.candles = self.candles[-self.max_candle_count():]

        return True

    def max_candle_count(self):
        return self.height - 3

    def last_candle_time(self):
        return self.candles[-1].time

    def render(self):
        title = "{} ({})".format(self.instrument, self.granularity)

        header = (
            "{:<{width[time]}} {:>{width[price]}} "
            "{:>{width[price]}} {:>{width[price]}} {:>{width[price]}} "
            "{:<{width[volume]}}"
        ).format(
            "Time",
            "Open",
            "High",
            "Low",
            "Close",
            "Volume",
            width=self.field_width
        )

        x = int((len(header) - len(title)) / 2)

        self.stdscr.addstr(
            0,
            x,
            title,
            curses.A_BOLD
        )

        self.stdscr.addstr(2, 0, header, curses.A_UNDERLINE)

        y = 3

        for candle in self.candles:
            time = candle.time.split(".")[0]
            volume = candle.volume

            for price in ["mid", "bid", "ask"]:
                c = getattr(candle, price, None)

                if c is None:
                    continue

                candle_str = (
                    "{:>{width[time]}} {:>{width[price]}} "
                    "{:>{width[price]}} {:>{width[price]}} "
                    "{:>{width[price]}} {:>{width[volume]}}"
                ).format(
                    time,
                    c.o,
                    c.h,
                    c.l,
                    c.c,
                    volume,
                    width=self.field_width
                )

                self.stdscr.addstr(y, 0, candle_str)

                y += 1

                break

        self.stdscr.move(0, 0)

        self.stdscr.refresh()


def price_to_str(price):
    return "{} ({}) {}/{}".format(
        price.instrument,
        price.time,
        price.bids[0].price,
        price.asks[0].price
    )


def heartbeat_to_str(heartbeat):
    return "HEARTBEAT ({})".format(
        heartbeat.time
    )
