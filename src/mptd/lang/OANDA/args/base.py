#!/usr/bin/env python3
from abc import ABC, abstractmethod


class ArgumentError(Exception):
    pass


class Argument(ABC):
    """
    Base class for OANDA argparser arguments
    """
    tag = None

    @staticmethod
    @abstractmethod
    def add(wrapper):
        pass

    @staticmethod
    @abstractmethod
    def parse(arg):
        pass
