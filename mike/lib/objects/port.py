from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from ryu.ofproto.ofproto_v1_3 import OFPPS_LINK_DOWN

from mike.lib.objects.interface import Interface
from mike.lib.objects.switch import Switch


class Port(Interface):
    '''
    {
        "uuid": UUID,
        "name": string,
        "number": integer,
        "switch": reference,
    }
    '''
    switch = models.ForeignKey(Switch, related_name="ports", null=False, editable=False)


class PortHwaddr(models.Model):
    port = models.ForeignKey(Port, related_name="hw_addrs", null=False, editable=False)
    hw_addr = models.CharField(max_length=12, null=False)  # ie. 1a2b3c4d5e6f

    class Meta:
        unique_together = (('port', 'hw_addr'))

