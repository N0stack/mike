from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

from mike.lib.objects.switch import Switch
from mike.lib.objects.interface import Interface


class Host(Interface):
    '''
    {
        "uuid": UUID,
        "name": string,
        "number": integer,
        "switch": reference,
        "hw_addr": string,
    }
    '''
    switch = models.ForeignKey(Switch, related_name="hosts", null=False, editable=False)
    hw_addr = models.CharField(max_length=12, null=True)  # ie. 1a2b3c4d5e6f

    def clean(self):
        super(Host, self).clean()
        if not self.switch.type == 'in' and not self.hw_addr:
            raise ValidationError(_('internal switch must have port with MAC address'))

        # TODO: valid mac address

    def __unicode__(self):
        return self.uuid
