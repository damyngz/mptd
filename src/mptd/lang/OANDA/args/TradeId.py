#!/usr/bin/env python3
from .base import Argument


class TradeID(Argument):

    tag = 'TradeID'

    @staticmethod
    def add(wrapper):
        wrapper.parser.add_argument(
            "tradeid",
            help=(
                "The ID of the Trade to create an Order for. If prepended "
                "with an '@', this will be interpreted as a client Trade ID"
            )
        )
        wrapper.param_parsers.append(lambda args: TradeID.parse(args))

    @staticmethod
    def parse(arg):
        if arg.trade_id is None:
            return None
        if arg.trade_id[0] == '@':
            return {"clientTradeID": arg.trade_id[1:]}
        else:
            return {"tradeID": arg.trade_id}

