from ryu.base import app_manager
from ryu.ofproto import ofproto_v1_3
from abc import ABCMeta, abstractmethod


DEFAULT_PRIORITY = 30000  # Layer 4
'''
Layer 2: 50000 ~ 59999
Layer 3: 40000 ~ 49999
Layer 4: 30000 ~ 39999
'''


class Service(metaclass=ABCMeta):
    '''
    this abstract class provides software designed service
    designed for connecting networks
    ex. l2sw, l3sw, napt route, firewall and so on
    '''

    def __init__(self, ryu_app):
        self._ryu_app = ryu_app

    @abstractmethod
    def add_port(self, port):
        '''
        add new port
        '''
        pass

    @abstractmethod
    def delete_port(self, port):
        '''
        delete port
        '''
        pass

    @abstractmethod
    def packet_in(self, event):
        '''
        this method called when packet in
        '''
        pass
