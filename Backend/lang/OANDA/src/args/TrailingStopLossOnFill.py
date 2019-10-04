#!/usr/bin/env python3
from .base import Argument
import v20.transaction


class TrailingStopLossOnFill(Argument):

    tag = 'TrailingStopLossOnFill'

    @staticmethod
    def add(wrapper):
        wrapper.parser.add_argument(
            "--trailing-stop-loss-distance", "--tsl",
            help=(
                "The price distance for the Trailing Stop Loss to add to a "
                "Trade opened by this Order"
            )
        )
        wrapper.param_parsers.append(lambda args: TrailingStopLossOnFill.parse(args))

    @staticmethod
    def parse(arg):
        if arg.stop_loss_distance is None:
            return None
        kwargs = {"price": arg.stop_loss_distance}
        return {"take_profit_on_fill": v20.transaction.TrailingStopLossDetails(**kwargs)}

