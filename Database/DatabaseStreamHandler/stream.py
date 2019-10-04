from abc import ABC, abstractmethod


class Stream(ABC):
    def __init__(self):
        self.ip_addr = None

    def ping(self):
        pass


class SubscriptionStream(Stream):
    def __init__(self):
        pass


class PollStream(Stream):
    def __init__(self):
        pass
