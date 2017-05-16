from mike.lib.objects.n0stack_object import N0stackObject
from mike.lib.uuid_objects import ModelUUIDObject

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from uuid import uuid4


class ModelSwitch(models.Model):
    '''
    {
        id: UUID,
        name: string,
        host_id: reference uuid,
        internal: boolean,
        datapath_id: integer,
        reference: manytomany reference,
    }
    '''
    SWITCH_TYPES = (
        (u'in', 'internal'),  # openvswitch internal port
        (u'ex', 'external'),  # openvswitch external port
        (u'ph', 'physical'),  # physical switch port
    )

    uuid = models.UUIDField(primary_key=True, editable=False)
    name = models.CharField(max_length=32, null=False)
    host_id = models.UUIDField(null=False, editable=False)
    type = models.CharField(null=False, editable=False, choices=SWITCH_TYPES)
    datapath_id = models.IntegerField(null=False)  # editable?
    services = models.ManyToManyField(ModelUUIDObject)

    class Meta:
        unique_together = (('host_id', 'datapath_id'))
        app_label = 'mike'

    def clean(self):
        if self.type is not 'ph' and not self.name:
            raise ValidationError(_('internal openvswitch interface is not seted name'))
        # checking that service is not n0stack object

    def __unicode__(self):
        return self.uuid


class Switches(N0stackObject):
    '''
    switch tool kits for mike base system
    '''

    model = ModelSwitch

    @classmethod
    def create_object(cls, host_id, internal):
        '''
        create openvswitch
        return (host_id, name)
        '''
        pass

    @classmethod
    def create(cls, host_id, type='in'):
        (datapath_id, name) = cls.create_object(host_id=host_id, internal=internal)
        return cls.add(name=name,
                       host_id=host_id,
                       internal=internal,
                       datapath_id=datapath_id)

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

        return new_switch
