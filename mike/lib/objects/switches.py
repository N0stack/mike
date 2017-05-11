from mike.models import ModelSwitch
from mike.lib.objects.n0stack_object import N0stackObject


class Switches(N0stackObject):
    '''
    switch tool kits for mike base system
    '''

    model = ModelSwitch

    @classmethod
    def add(cls, name, host_id, datapath_id, internal=True):
        '''
        add switch for mike base system
        '''
        new_switch = ModelSwitch(name=name,
                                 host_id=host_id,
                                 internal=internal,
                                 datapath_id=datapath_id)
        new_switch.save()

        return new_switch.uuid
