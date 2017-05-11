from mike.lib.objects.n0stack_object import N0stackObject
from mike.lib.objects.switches import ModelSwitch

from django.db import models
from uuid import uuid4


class ModelPort(models.Model):
    '''
    {
        id: UUID,
        name: string,
        number: integer,
        network: reference,
        switch: reference,
        mac_addr: integer,
        dhcp: boolean,
        ipv4_ip_addr: integer,
        ipv4_subnet_mask: integer,
    }
    '''
    uuid = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    number = models.IntegerField(null=False)
    name = models.CharField(max_length=32, default='')  # empty means switch is physical
    # network = models.ForeignKey(ModelNetwork, related_name="ports")
    switch = models.ForeignKey(ModelSwitch, related_name="ports", null=False, editable=False)
    mac_addr = models.CharField(max_length=17, null=False)
    ipv4_addr = models.CharField(max_length=11)
    ipv4_subnet_mask = models.CharField(max_length=11)

    class Meta:
        unique_together = (('switch', 'number'))  # 要確認
        app_label = 'mike'

    def __unicode__(self):
        return self.uuid


class Ports(N0stackObject):
    model = ModelPort

    @classmethod
    def add(cls,
            number,
            switch,
            mac_addr,
            name='',
            ipv4_addr=None,
            ipv4_subnet_mask=None):
        # Noneでdefaultが適用されるのか？
        if ipv4_addr and ipv4_subnet_mask:
            new_port = ModelPort(number=number,
                                 name=name,
                                 switch=switch,
                                 mac_addr=mac_addr,
                                 ipv4_addr=ipv4_addr,
                                 ipv4_subnet_mask=ipv4_subnet_mask)
        elif not ipv4_addr and not ipv4_subnet_mask:
            new_port = ModelPort(number=number,
                                 name=name,
                                 switch=switch,
                                 mac_addr=mac_addr)
        else:
            raise Exception
        new_port.save()

        return new_port.uuid
