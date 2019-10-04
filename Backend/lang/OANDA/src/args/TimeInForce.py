#!/usr/bin/env python3
from .base import Argument, ArgumentError


class TimeInForce(Argument):

    tag = 'TimeInForce'

    @staticmethod
    def add(wrapper, choices=None):
        if choices is None:
            choices = ["FOK", "IOC", "GTC", "GFD", "GTD"]

        wrapper.parser.add_argument(
            "--time-in-force", "--tif",
            choices=choices,
            help="The time-in-force to use for the Order"
        )

        # GTD Good till Date
        if "GTD" in choices:
            wrapper.parser.add_argument(
                "--gtd-time",
                help=(
                    "The date to use when the time-in-force is GTD. "
                    "Format is 'YYYY-MM-DD HH:MM:SS"
                )
            )

        wrapper.param_parsers.append(lambda args: TimeInForce.parse(args))

    @staticmethod
    def parse(arg):
        outp = {}
        if arg.time_in_force is None:
            return None

        outp["time_in_force"] = arg.time_in_force

        if arg.time_in_force == "GTD":
            try:
                if arg.gtd_time is None:
                    raise ArgumentError
            except ArgumentError:
                print("must set --gtd-time \"YYYY-MM-DD HH:MM:SS\" when "
                      "--time-in-force=GTD")

            # TODO dateTime formatter for this value
            outp['gtd_time'] = arg.gtd_time

        return outp
