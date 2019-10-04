#!/usr/bin/env python3
from .base import Argument


class Units(Argument):

    tag = 'Units'

    @staticmethod
    def add(wrapper):
        wrapper.parser.add_argument(
            "units",
            help=(
                "The number of units for the Order. "
                "Negative values indicate sell, Positive values indicate buy"
            )
        )
        wrapper.param_parsers.append(lambda args: Units.parse(args))

    @staticmethod
    def parse(arg):
        if arg.units is None:
            return None
        return {"units": arg.instrument}

