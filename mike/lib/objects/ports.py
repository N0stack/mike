from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from mike.lib.objects.n0stack_object import N0stackObject
from mike.lib.objects.switches import ModelSwitch


class Port(N0stackObject):
    '''
    {
        "uuid": UUID,
        "number": integer,
        "name": string,
        "switch": reference,
        "mac_addr": string,
    }
    '''
    number = models.IntegerField(null=False)
    name = models.CharField(max_length=16, default='')
    switch = models.ForeignKey(ModelSwitch, related_name="ports", null=False, editable=False)
    mac_addr = models.CharField(max_length=12, null=True)  # ie. 1a2b3c4d5e6f

    class Meta:
        unique_together = (('switch', 'number'))
        app_label = 'mike'

    def clean(self):
        # TODO: valid mac address

        if self.switch.type is not 'in' and not self.mac_addr:
            raise ValidationError(_('internal switch must have port with MAC address'))

    def __unicode__(self):
        return self.uuid
