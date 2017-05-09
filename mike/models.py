from django.db import models


# class ModelNetwork(models.Model):
#     '''
#     {
#         id: integer,
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
        id: integer,
        name: string,
        host_id: reference uuid,
        internal: boolean,
        datapath_id: integer,
    }
    '''
    uuid = models.UUIDField(auto=True, primary_key=True, editable=False)
    name = models.CharField(len=32, null=False)
    host_id = models.UUIDField(null=False, editable=False)
    internal = models.BooleanField(null=False, editable=False)
    datapath_id = models.IntegerField(null=False)  # editable?


class ModelPort(models.Model):
    '''
    {
        id: integer,
        name: string,
        network: reference,
        switch: reference,
        mac_addr: string,
        ipv4_ip_addr: string, # "dhcp" / ip
        ipv4_subnet_mask: string,
    }
    '''
    uuid = models.UUIDField(auto=True, primary_key=True, editable=False)
    name = models.CharField(len=32)
    # network = models.ForeignKey(ModelNetwork, related_name="ports")
    switch = models.ForeignKey(ModelSwitch, related_name="ports")
    mac_addr = models.CharField(len=12)
    ipv4_addr = models.CharField(len=11)
    ipv4_subnet_mask = models.CharField(len=11)


class ModelSwitchLink(models.Model):
    '''
    {
        id: integer,
        name: string
        counter_link: reference,
        switch: reference,
    }
    '''
    name = models.CharField(len=32)
    counter_link = models.OneToOneField(self)
    switch = models.ForeignKey(ModelSwitch, related_name="switch_links")


# class ModelFloatingIp(models.Model):
#     '''
#     {
#         id: integer,
#         host_id: reference,
#         port_id: reference,
#         ip: string, # "dhcp" / "ip"
#     }
#     '''
