from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from ryu.ofproto.ofproto_v1_3 import OFPPS_LINK_DOWN

<<<<<<< HEAD
from mike.lib.objects.interface import Interface
from mike.lib.objects.switch import Switch
=======
from mike.lib.mike_object import MikeObject
>>>>>>> 1a23f6f502a9b8185c4cbe35ca856a17d093efd9


class Port(Interface):
    '''
    {
        "uuid": UUID,
        "name": string,
        "number": integer,
        "switch": reference,
    }
    '''
<<<<<<< HEAD
    switch = models.ForeignKey(Switch, related_name="ports", null=False, editable=False)
=======
    name = models.CharField(max_length=16, null=False, blank=True)
    number = models.IntegerField(null=True)
    state = models.IntegerField(default=OFPPS_LINK_DOWN, null=False)
>>>>>>> 1a23f6f502a9b8185c4cbe35ca856a17d093efd9


class PortHwaddr(models.Model):
    port = models.ForeignKey(Port, related_name="hw_addrs", null=False, editable=False)
    hw_addr = models.CharField(max_length=12, null=False)  # ie. 1a2b3c4d5e6f

    class Meta:
        unique_together = (('port', 'hw_addr'))

