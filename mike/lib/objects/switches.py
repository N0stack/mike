from mike.lib.objects.n0stack_object import N0stackObject

from django.db import models
from uuid import uuid4


class ModelSwitch(models.Model):
    '''
    {
        id: UUID,
        name: string,
        host_id: reference uuid,
        internal: boolean,
        datapath_id: integer,
    }
    '''
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=32, null=False)
    host_id = models.UUIDField(null=False, editable=False)
    internal = models.BooleanField(null=False, editable=False, default=True)
    datapath_id = models.IntegerField(null=False)  # editable?

    class Meta:
        unique_together = (('host_id', 'datapath_id'))
        app_label = 'mike'

    def __unicode__(self):
        return self.uuid


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
