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
            t = UUIDObjectType.objects.filter(name=self.__class__.__name__)[0]
            self.uuid_object = UUIDObject(object_type=t)
            self.uuid_object.save()

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

    @abstractmethod
    def add_port(self, ev, port, app):
        '''
        add new port
        this method prepared for mike.controller.openflow
        '''
        pass

    @abstractmethod
    def delete_port(self, ev, port, app):
        '''
        delete port
        this method prepared for mike.controller.openflow
        '''
        pass

    @abstractmethod
    def modify_port(self, ev, port, app):
        '''
        modify port
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

    def packet_in(self, ev, app):
        '''
        this method called when packet in
        this method prepared for mike.controller.openflow
        '''
        raise NotImplementedError()

    def removed_flow(self, ev, app):
        '''
        this method called when flow removed
        this method prepared for mike.controller.openflow
        '''
        raise NotImplementedError()

    @abstractmethod
    def init_ports(self, ev, switch, app):
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

