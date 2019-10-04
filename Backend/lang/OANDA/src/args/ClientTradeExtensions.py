#!/usr/bin/env python3
from .base import Argument


class ClientTradeExtensions(Argument):

    tag = 'ClientTradeExtensions'

    @staticmethod
    def add(wrapper):
        raise NotImplementedError

    @staticmethod
    def parse(arg):
        if arg is None:
            return None
        raise NotImplementedError

