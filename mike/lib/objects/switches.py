from mike.models import ModelSwitch
from mike.exceptions import ExceptionAlreadyExists
from mike.lib.objects.n0stack_object import N0stackObject


class Switches(N0stackObject):
    '''
    switch tool kits for mike base system
    '''

    object_model = ModelSwitch

    @classmethod
    def add(cls, name, host_id, datapath_id, internal=None):
        '''
        add switch for mike base system
        '''
        if internal:
            new_switch = ModelSwitch(name=name,
                                     host_id=host_id,
                                     internal=internal,
                                     datapath_id=datapath_id)
        else:
            new_switch = ModelSwitch(name=name,
                                     host_id=host_id,
                                     datapath_id=datapath_id)

        try:
            new_switch.save()
        except:  # exception type 要調査
            msg = ""
            raise ExceptionAlreadyExists(msg)
        return cls(new_switch.uuid)
