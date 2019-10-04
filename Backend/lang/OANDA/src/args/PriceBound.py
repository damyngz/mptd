#!/usr/bin/env python3
from .base import Argument


class PriceBound(Argument):

    tag = 'PriceBound'

    @staticmethod
    def add(wrapper):
        wrapper.parser.add_argument(
            "--price-bound", "-b",
            help="The worst price bound allowed for the Order"
        )
        wrapper.param_parsers.append(lambda args: PriceBound.parse(args))

    @staticmethod
    def parse(arg):
        if arg.price_bound is None:
            return None

        return {"price_bound": arg.price_bound}

