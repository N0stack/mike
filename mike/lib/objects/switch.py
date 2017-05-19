from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from mike.lib.mike_object import MikeObject, UUIDObject


class Switch(MikeObject):
    '''
    {
        "uuid": UUID,
        "name": string,
        "host_id": uuid,
        "type": 'in' / 'ex' / 'ph',
        "datapath_id": integer,
        "services": manytomany reference,
    }
    '''
    SWITCH_TYPES = (
        (u'in', 'internal'),  # openvswitch internal port
        (u'ex', 'external'),  # openvswitch external port
        (u'ph', 'physical'),  # physical switch port
    )

    name = models.CharField(max_length=32, null=False)
    host_id = models.UUIDField(null=False, editable=False)
    type = models.CharField(max_length=2, null=False, editable=False, choices=SWITCH_TYPES)
    datapath_id = models.IntegerField(null=False)
    services = models.ManyToManyField(UUIDObject)

    class Meta:
        unique_together = (('host_id', 'datapath_id'))

    def clean(self):
        if not self.type == 'ph' and not self.name:
            raise ValidationError(_('internal openvswitch interface is not seted name'))
        # checking that service is not n0stack object

    def __unicode__(self):
        return self.uuid

# def create_switch(host_id):