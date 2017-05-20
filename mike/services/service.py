from abc import ABCMeta, abstractmethod

from mike.lib.mike_object import UUIDObject, UUIDObjectType


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

    def __init__(self, uuid):
        '''
        register UUIDObject and generate uuid
        '''
        if uuid:
            self.uuid_object = UUIDObject(uuid=uuid)
        else:
            t = UUIDObjectType.objects.filter(name=self.__class__.__name__)
            self.uuid_object = UUIDObject(type=t)
            self.uuid_object.save()

    @abstractmethod
    def generate_flow(self, *args, **kwargs):
        '''
        this method prepared for uppper layer
        return [(datapath, match, actions)]
        '''
        pass

    @abstractmethod
    def add_host(self, ev, host, app):
        '''
        add new host
        this method prepared for mike.controller.openflow
        '''
        pass

    @abstractmethod
    def delete_host(self, ev, host, app):
        '''
        delete host
        this method prepared for mike.controller.openflow
        '''
        pass

    @abstractmethod
    def modify_host(self, ev, host, app):
        '''
        modify host
        this method prepared for mike.controller.openflow
        '''
        pass

    @abstractmethod
    def add_link(self, ev, link, app):
        '''
        add new link
        this method prepared for mike.controller.openflow
        '''
        pass

    @abstractmethod
    def delete_link(self, ev, link, app):
        '''
        delete link
        this method prepared for mike.controller.openflow
        '''
        pass

    @abstractmethod
    def modify_link(self, ev, link, app):
        '''
        modify link
        changed link status
        this method prepared for mike.controller.openflow
        '''
        pass

    def add_switch(self, switch):
        '''
        this method prepared for web API
        '''
        switch.services.add(self.uuid_object)

    def delete_switch(self, switch):
        '''
        this method prepared for web API
        '''
        switch.services.remove(self.uuid_object)

    def packet_in(self, ev, app):
        '''
        this method called when packet in
        this method prepared for mike.controller.openflow
        '''
        raise NotImplementedError()

    @abstractmethod
    def reinit_ports(self, ev, switch, app):
        '''
        this method called when switch registered
        check and initilize objects
        this method prepared for mike.controller.openflow
        '''
        pass

    def delete(self):
        '''
        delete self
        '''
        raise NotImplementedError()

