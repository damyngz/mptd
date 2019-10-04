#!/usr/bin/env python3


class Account(object):
    def __init__(self, account, transaction_cache_depth=100):
        self.trades = {}
        self.orders = {}
        #
        self.order_states = {}
        self.order_states = {}
        self.positions = {}
        #
        self.transaction_cache_depth = transaction_cache_depth
        self.transactions = []
        #
        self.details = account
        #
        for trade in getattr(account, "trades", []):
            self.trades[trade.id] = trade

        for order in getattr(account, "orders", []):
            self.orders[order.id] = order

        for position in getattr(account, "positions", []):
            self.positions[position.instrument] = position
        setattr(account, "positions", None)

    def dump(self):
        pass

    def order_get(self):
        pass

    def trade_get(self):
        pass

    def position_get(self):
        pass

    # TODO
    # TODO apply trade states
    # TODO account changes
    # TODO NotImplemented
    #


def account_status(api,
                   account_id):

    response = api.account.get(account_id)
    account = Account(response.get("account", "200"))

