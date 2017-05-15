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
    def generate_flow(self, *args, **kwargs):
        '''
        return {
            datapath: (
                match,
                actions
            )
        }
        '''
        pass

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
    def add_switch(self, switch):
        '''
        add switch
        '''
        pass

    @abstractmethod
    def delete_switch(self, switch):
        '''
        delete switch
        '''
        pass

    @abstractmethod
    def packet_in(self, event):
        '''
        this method called when packet in
        '''
        pass
