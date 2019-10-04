#!/usr/bin/env python3
from .base import Argument
import v20.transaction


class StopLossOnFill(Argument):

    tag = 'StopLossOnFill'

    @staticmethod
    def add(wrapper):
        wrapper.parser.add_argument(
            "--stop-lose-price", "--sl",
            help=(
                "The price of the Stop Loss to add to a Trade opened by this "
                "Order"
            )
        )
        wrapper.param_parsers.append(lambda args: StopLossOnFill.parse(args))

    @staticmethod
    def parse(arg):
        if arg.stop_loss_price is None:
            return None
        kwargs = {"price": arg.stop_loss_price}
        return {"take_profit_on_fill": v20.transaction.StopLossDetails(**kwargs)}

