#!/usr/bin/env python3
from .base import Argument


class ShortUnits(Argument):

    tag = 'ShortUnits'

    @staticmethod
    def add(wrapper):

        wrapper.parser.add_argument(
            "--short-units",
            default=None,
            help=(
                "The amount of the short Position to close. Either the string "
                "'ALL' indicating a full Position close, the string 'NONE', or the "
                "number of units of the Position to close"
            )
        )
        wrapper.param_parsers.append(lambda args: ShortUnits.parse(args))

    @staticmethod
    def parse(arg):
        if arg.short_units is None:
            return None
        return {"short_units": arg.short_units}

