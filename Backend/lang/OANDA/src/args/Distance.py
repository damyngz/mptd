#!/usr/bin/env python3
from .base import Argument


class Distance(Argument):

    tag = 'Distance'

    @staticmethod
    def add(wrapper):
        wrapper.parser.add_argument(
            "distance",
            help="The price distance for the Order"
        )
        wrapper.param_parsers.append(lambda args: Distance.parse(args))

    @staticmethod
    def parse(arg):
        if arg.distance is None:
            return None
        return {"distance": arg.distance}
