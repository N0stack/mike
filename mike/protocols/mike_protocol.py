from abc import ABCMeta, abstractmethod


class MikeProtocol(metaclass=ABCMeta):
    def __init__(data_path, self):
        self.data_path = data_path

    @abstractmethod
    def inbound(self):
        pass

    @abstractmethod
    def outbound(self):
        pass