#!/usr/bin/env python3
from .base import Argument


class PositionFill(Argument):

    tag = 'PositionFill'
    @staticmethod
    def add(wrapper, choices=None):
        if choices is None:
            choices = ["DEFAULT", "OPEN_ONLY", "REDUCE_FIRST", "REDUCE_ONLY"]

        wrapper.parser.add_argument(
            "--position-fill",
            help="Specification of how the Order may affect open positions."
        )
        wrapper.param_parsers.append(lambda args: PositionFill.parse(args))

    @staticmethod
    def parse(arg):
        if arg.position_fill is None:
            return None

        return {"position_fill": arg.position_fill}

