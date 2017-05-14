from mike.lib.objects.n0stack_object import N0stackObject
from mike.lib.objects.switches import ModelSwitch

from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from ryu.lib.ip import valid_ipv4
from uuid import uuid4


class ModelPort(models.Model):
    '''
    {
        "id": UUID,
        "name": string,
        "number": integer,
        "network": reference,
        "switch": reference,
        "mac_addr": string,
    }
    '''
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    number = models.IntegerField(null=False)
    name = models.CharField(max_length=32, default='')  # empty means switch is physicaly
    # network = models.ForeignKey(ModelNetwork, related_name="ports") ManyToMany?
    switch = models.ForeignKey(ModelSwitch, related_name="ports", null=False, editable=False)
    mac_addr = models.CharField(max_length=17, null=True)

    class Meta:
        unique_together = (('switch', 'number'))
        app_label = 'mike'

    def clean(self):
        # valid mac address

        if self.switch.type is not 'in' and not self.mac_addr:
            raise ValidationError(_('internal switch must have port with MAC address'))

    def __unicode__(self):
        return self.uuid


class Ports(N0stackObject):
    model = ModelPort

    @classmethod
    def create_object(cls, switch):
        '''
        create port to openvswitch
        return (port_number, port_name)
        '''
        if not switch.name:
            raise  # this is physical switch, so cannot create the port

    @classmethod
    def create(cls, switch, mac_addr):
        (num, name) = cls.create_object(switch=switch)
        return cls.add(number=num,
                       name=name,
                       switch=switch,
                       mac_addr=mac_addr)

    @classmethod
    def add(cls,
            number,
            switch,
            mac_addr,
            name=''):
        new_port = ModelPort(number=number,
                             name=name,
                             switch=switch,
                             mac_addr=mac_addr)
        new_port.save()

        return new_port
