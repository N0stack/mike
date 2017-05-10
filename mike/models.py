from django.db import models
from uuid import uuid4


# class ModelNetwork(models.Model):
#     '''
#     {
#         id: UUID,
#         name: string,
#         serivce: reference
#         network_group_id: reference,  # stay
#         dhcp: {
#             ip_start: string,
#             ip_end: string,
#             subnet_mask: string,
#             gateway: string,
#             dns: [
#             string,
#             ],
#             options: [
#             {
#                 key: integer,
#                 value: string
#             }
#             ]
#         },
#     }
#     '''
#     uuid = models.UUIDField(auto=True, primary_key=True, editable=False)
#     name = models.CharField(len=128)


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
    uuid = models.UUIDField(primary_key=True, default=uuid4(), editable=False)
    name = models.CharField(max_length=32, null=False)
    host_id = models.UUIDField(null=False, editable=False)
    internal = models.BooleanField(null=False, editable=False, default=True)
    datapath_id = models.IntegerField(null=False)  # editable?

    class Meta:
        unique_together = (('host_id', 'datapath_id'))

    def __unicode__(self):
        return self.uuid


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
    uuid = models.UUIDField(primary_key=True, default=uuid4(), editable=False)
    number = models.IntegerField(null=False)
    name = models.CharField(max_length=32)
    # network = models.ForeignKey(ModelNetwork, related_name="ports")
    switch = models.ForeignKey(ModelSwitch, related_name="ports")
    mac_addr = models.CharField(max_length=17)
    ipv4_addr = models.CharField(max_length=11)
    ipv4_subnet_mask = models.CharField(max_length=11)

    class Meta:
        unique_together = (('switch', 'number'))  # 要確認

    def __unicode__(self):
        return self.uuid


class ModelSwitchLink(models.Model):
    '''
    {
        id: integer,
        name: string,
        number: integer,
        next_link: reference,
        switch: reference,
    }
    '''
    uuid = models.UUIDField(primary_key=True, default=uuid4(), editable=False)
    name = models.CharField(max_length=32)
    number = models.IntegerField(null=False)
    next_link = models.OneToOneField('self')
    switch = models.ForeignKey(ModelSwitch, related_name="switch_links")

    class Meta:
        unique_together = (('switch', 'next_link'))


# class ModelFloatingIp(models.Model):
#     '''
#     {
#         id: integer,
#         host_id: reference,
#         port_id: reference,
#         ip: string, # "dhcp" / "ip"
#     }
#     '''
