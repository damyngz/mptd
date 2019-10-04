#!/usr/bin/env python3
from .base import Argument


class Price(Argument):

    tag = 'Price'
    @staticmethod
    def add(wrapper):
        wrapper.parser.add_argument(
            "price",
            help="The price threshold for the Order"
        )
        wrapper.param_parsers.append(lambda args: Price.parse(args))

    @staticmethod
    def parse(arg):
        if arg.price is None:
            return None
        return {"price": arg.price}
