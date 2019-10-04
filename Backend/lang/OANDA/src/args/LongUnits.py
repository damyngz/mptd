#!/usr/bin/env python3
from .base import Argument


class LongUnits(Argument):

    tag = 'LongUnits'

    @staticmethod
    def add(wrapper):

        wrapper.parser.add_argument(
            "--long-units",
            default=None,
            help=(
                "The amount of the long Position to close. Either the string 'ALL' "
                "indicating a full Position close, the string 'NONE', or the "
                "number of units of the Position to close"
            )
        )
        wrapper.param_parsers.append(lambda args: LongUnits.parse(args))

    @staticmethod
    def parse(arg):
        if arg.long_units is None:
            return None
        return {"long_units": arg.long_units}

