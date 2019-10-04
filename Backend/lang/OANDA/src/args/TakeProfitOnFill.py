#!/usr/bin/env python3
from .base import Argument
import v20.transaction


class TakeProfitOnFill(Argument):

    tag = 'TakeProfitOnFill'

    @staticmethod
    def add(wrapper):
        wrapper.parser.add_argument(
            "--take-profit-price", "--tp",
            help=(
                "The price of the Take Profit to add to a Trade opened by this "
                "Order"
            )
        )
        wrapper.param_parsers.append(lambda args: TakeProfitOnFill.parse(args))

    @staticmethod
    def parse(arg):
        if arg.take_profit_price is None:
            return None
        kwargs = {"price": arg.take_profit_price}
        return {"take_profit_on_fill": v20.transaction.TakeProfitDetails(**kwargs)}
