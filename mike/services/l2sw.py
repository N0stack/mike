from ryu.app.ofctl.api import get_datapath
from django.db import models

from mike.controller.openflow import MikeOpenflowController
from mike.services.service import Service
from mike.services.service import Hub
from mike.lib.objects.switch import Switch
from mike.lib.objects.link import Link
from mike.lib.objects.host import Host


SERVICE_L2SW_PRIORITY = 20001  # Layer 2
SERVICE_L2SW_PACKETIN_PRIORITY = 2001  # Layer 2


class ServiceL2swTable(models.Model):
    l2sw = models.UUIDField(editable=False, null=False)
    vlan_id = models.UUIDField(editable=False, null=False)
    hub = models.UUIDField(editable=False, null=False, unique=True)

    class Meta:
        unique_together = (('l2sw', 'vlan_id'))
        app_label = 'mike'


class L2sw(Service):
    '''
    l2sw separate network by vlan

    support:
      - internal to internal
      - internal to external
      - internal to internal of otherhost (tunneling)
      - external to internal
      - external to external
    '''

    def __init__(self, uuid=None):
        super(L2sw, self).__init__(uuid)
        self.objects = ServiceL2swTable.objects.filter(l2sw=self.uuid_object.uuid)

    def add_network(self, vlan_id):
        '''
        add vlan network
        '''
        h = Hub()
        network = ServiceL2swTable(l2sw=self.uuid_object.uuid,
                                   vlan_id=vlan_id,
                                   hub=h.uuid_object)
        network.save()

    def delete_network(self, vlan_id):
        '''
        delete vlan network
        '''
        network = self.objects.filter(vlan_id=vlan_id)
        if not network:
            # TODO: replace Exception
            raise Exception('there is no network vlan_id=%d, uuid=%s' %
                            (vlan_id, self.uuid_object.uuid))
        Hub(network[0].hub.uuid).delete()
        network[0].delete()

    def add_host(self, ev, host, app):
        pass

    def delete_host(self, ev, host, app):
        pass

    def modify_host(self, ev, host, app):
        pass

    def add_link(self, ev, link, app):
        pass

    def delete_link(self, ev, link, app):
        pass

    def modify_link(self, ev, link, app):
        pass

    def add_switch(self, switch):
        switch.services.add(self.uuid_object)

    def delete_switch(self, switch):
        switch.services.remove(self.uuid_object)

    cookies = {}
    '''
    cookies[cookie] = vlan_id
    '''

    def packet_in(self, ev, app):
        vlan_id = self.cookies[ev.msg.cookie]
        network = self.objects.filter(vlan_id=vlan_id)

        network.hub.packet_in(ev, app)

    def reinit_ports(self, ev, switch, app):
        if not switch.type == 'ex':
            return
        # send CONTROLLER
        for network in self.objects.all():
            network.hub.reinit_ports(ev, switch, app)

            cookie = MikeOpenflowController.add_packet_in_hook(self.uuid_object.uuid)
            self.cookies[cookie] = network.vlan_id

            ofproto = ev.dp.ofproto
            parser = ev.dp.ofproto_parser
            match = parser.OFPMatch(vlan_vid=(0x1000 | network.vlan_id))
            actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                              ofproto.OFPCML_NO_BUFFER)]
            i = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
            mod = parser.OFPFlowMod(datapath=ev.dp,
                                    priority=SERVICE_L2SW_PACKETIN_PRIORITY,
                                    cookie=cookie,
                                    table_id=0,
                                    match=match,
                                    instructions=i)
            ev.dp.send_msg(mod)

    def delete(self):
        pass
