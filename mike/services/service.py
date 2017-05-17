from abc import ABCMeta, abstractmethod


DEFAULT_PRIORITY = 30000  # Layer 4
'''
Layer 2: 20000 ~ 9999
Layer 3: 30000 ~ 9999
Layer 4: 40000 ~ 9999
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
    def add_port(self, ev, port, app):
        '''
        add new port
        '''
        pass

    @abstractmethod
    def delete_port(self, ev, port, app):
        '''
        delete port
        '''
        pass

    @abstractmethod
    def modify_port(self, ev, port, app):
        '''
        modify port
        changed port status
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
    def packet_in_handler(self, ev, app):
        '''
        this method called when packet in
        '''
        pass

    @abstractmethod
    def reinit_ports(self, ev, switch, app):
        '''
        this method called when switch registered
        check and initilize objects
        '''
        pass
