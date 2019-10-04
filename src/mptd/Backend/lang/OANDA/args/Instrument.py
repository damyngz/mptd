#!/usr/bin/env python3
from .base import Argument


class Instrument(Argument):

    tag = 'Instrument'

    @staticmethod
    def add(wrapper):

        def _filter(arg):
            return arg.replace("/", "_")

        wrapper.parser.add_argument(
            "instrument",
            type=_filter,
            help="The instrument to place the Order for"
        )
        wrapper.param_parsers.append(lambda args: Instrument.parse(args))

    @staticmethod
    def parse(arg):
        if arg.instrument is None:
            return None
        return {"instrument": arg.instrument}

