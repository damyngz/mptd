#!/usr/bin/env python3

import logging
from abc import ABC, abstractclassmethod
from args import *


def _concat(args_dict):
    parsed_args_dict = {}
    for arg in args_dict:
        if arg is not None:
            parsed_args_dict = {**parsed_args_dict, **arg}
    return parsed_args_dict


def close_order(api,
                trade_id,
                units=None):

    args = {}
    if units:
        args['units'] = units

    response = api.context.order.market(api.config.active_account, **args)
    return response


def market_order(api,
                 instrument,
                 units,
                 time_in_force=None,
                 price_bound=None,
                 position_fill=None,
                 take_profit_on_fill=None,
                 stop_loss_on_fill=None,
                 client_order_extensions=None,
                 client_trade_extensions=None):

    optional_args = [TimeInForce.parse(time_in_force),
                     PriceBound.parse(price_bound),
                     PositionFill.parse(position_fill),
                     TakeProfitOnFill.parse(take_profit_on_fill),
                     StopLossOnFill.parse(stop_loss_on_fill),
                     ClientTradeExtensions.parse(client_order_extensions),
                     ClientTradeExtensions.parse(client_trade_extensions)]

    args = {'instrument': Instrument.parse(instrument), 'units': Units.parse(units)}
    args = {**args, **_concat(optional_args)}

    response = api.context.order.market(api.config.active_account, **args)
    return response


def take_profit_order():
    raise NotImplementedError


def stop_loss_order():
    raise NotImplementedError


def trailing_stop_loss_order():
    raise NotImplementedError
