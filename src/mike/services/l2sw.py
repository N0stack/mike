from django.db import models

from mike.controller.openflow import MikeOpenflowController
from mike.services.service import Service
from mike.services.hub import Hub


SERVICE_L2SW_PRIORITY = 20001  # Layer 2
SERVICE_L2SW_PACKET_IN_PRIORITY = 2001  # Layer 2


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
      - internal to internal of otherport (tunneling)
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

    def add_port(self, ev, port, app):
        pass

    def delete_port(self, ev, port, app):
        pass

    def modify_port(self, ev, port, app):
        pass

    def add_link(self, ev, link, app):
        pass

    def delete_link(self, ev, link, app):
        pass

    def modify_link(self, ev, link, app):
        pass

    cookies = {}
    '''
    cookies[cookie] = vlan_id
    '''

    def init_ports(self, ev, switch, app):
        if not switch.type == 'ex':
            return
        # send CONTROLLER
        for network in self.objects.all():
            cookie = MikeOpenflowController.hook_packet_in(self.uuid_object.uuid)
            self.cookies[cookie] = network.hub.uuid_object.uuid

            datapath = ev.dp
            ofproto = datapath.ofproto
            parser = datapath.ofproto_parser

            match = parser.OFPMatch(vlan_vid=(0x1000 | network.vlan_id))
            inst = [parser.OFPInstructionWriteMetadata(network.hub.metadata, network.hub.METADATA_MASK),
                    parser.OFPInstructionGotoTable(network.hub.SRC_TABLE)]
            mod = parser.OFPFlowMod(datapath=datapath,
                                    priority=SERVICE_L2SW_PACKET_IN_PRIORITY,
                                    command=ofproto.OFPFC_ADD,
                                    match=match,
                                    instructions=inst)
            datapath.send_msg(mod)

            actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                              ofproto.OFPCML_NO_BUFFER)]
            i = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
            mod = parser.OFPFlowMod(datapath=datapath,
                                    priority=SERVICE_L2SW_PACKET_IN_PRIORITY,
                                    cookie=cookie,
                                    table_id=0,
                                    match=match,
                                    instructions=i)
            datapath.send_msg(mod)

    def delete(self):
        pass
