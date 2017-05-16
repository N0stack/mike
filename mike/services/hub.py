from ryu.app.ofctl.api import get_datapath
from django.db import models
from uuid import uuid4
import logger

from mike.services.service import Service
from mike.models import ModelPort, ModelSwitchLink


SERVICE_HUB_PRIORITY = 20000  # Layer 2


class ModelServiceHubTable(models.Model):
    hub = models.UUIDField(editable=False, null=False)
    port = models.ForeignKey(ModelPort, related_name="service_hub_table", null=False)

    class Meta:
        unique_together = (('hub', 'port'))
        app_label = 'mike'


class Hub(Service):
    '''
    simple switching hub

    support:
      - internal to internal
      - internal to external
      - external to internal
      - internal to internal of otherhost (tunneling)
    not support:
      - external to external
    '''

    def __init__(self, ryu_app, uuid=None):
        super(Hub, self).__init__(ryu_app)
        if uuid:
            self.uuid = uuid
        else:
            self.uuid = uuid4
        # self.logger = logger

    def generate_flow(self, port):
        if port.switch.type in 'in':
            self._generate_internal_flow(port)
        else:
            self._generate_external_flow(port)

    def _generate_internal_flow(self, port):
        flows = {}
        ports = ModelServiceHubTable.objects.all().filter(hub=self.uuid)
        for dst_port in ports:
            if not port.switch.host_id == dst_port.switch.host_id:
                '''
                tunneling
                '''
            if port.switch.datapath_id == dst_port.switch.datapath_id:
                '''
                internal to internal
                '''
                datapath = get_datapath(self._ryu_app,
                                        port.switch.datapath_id)
                parser = datapath.ofproto_parser
                match = parser.OFPMatch(in_port=port.number,
                                        eth_dst=dst_port.mac_address)
                actions = [parser.OFPActionOutput(dst_port.number)]
                flows[port.switch.datapath] = (match, actions)
            else:
                '''
                internal to external
                '''
                in_link = ModelSwitchLink.objects.all().filter(switch__uuid=port.switch.uuid,
                                                               next_link__uuid=dst_port.switch.uuid)[0]

                datapath = get_datapath(self._ryu_app,
                                        port.switch.datapath_id)
                parser = datapath.ofproto_parser
                match = parser.OFPMatch(in_port=port.number,
                                        eth_dst=dst_port.mac_address)
                actions = [parser.OFPActionOutput(in_link.number)]
                flows[port.switch.datapath] = (match, actions)

                # secondary switch
                datapath = get_datapath(self._ryu_app,
                                        dst_port.switch.datapath_id)
                parser = datapath.ofproto_parser
                match = parser.OFPMatch(in_port=in_link.next_link.number,
                                        eth_dst=dst_port.mac_address)
                actions = [parser.OFPActionOutput(dst_port.number)]
                flows[datapath] = (match, actions)
        return flows

    def _generate_external_flow(self, port):
        '''
        external to internal
        '''
        ports = ModelServiceHubTable.objects.all().filter(hub=self.uuid)

    def add_port(self, port):
        self._learn_mac_address(port)
        for k, v in self.generate_flow(port):
            self._send_flow(k, v[0], v[1])

    def delete_port(self, port):
        pass

    def switch_features_handler(self, event):
        pass

    def packet_in_handler(self, event):
        pass

    def _learn_mac_address(self, port):
        '''
        learning mac address
        '''
        new_query = ModelServiceHubTable(hub=self.uuid,
                                         port=port)
        new_query.save()
        # self.logger.info("[add mac table] dpid: %s, src_address: %s, inport: %s service: %s",
        #                  port.switch.dpid,
        #                  port.mac_address,
        #                  port.name,
        #                  self.uuid)

    def _send_flow(self, datapath, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        instruction = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                                    actions)]

        if buffer_id:
            flow_mod = parser.OFPFlowMod(datapath=datapath,
                                         buffer_id=buffer_id,
                                         priority=SERVICE_HUB_PRIORITY,
                                         match=match,
                                         instructions=instruction)
        else:
            flow_mod = parser.OFPFlowMod(datapath=datapath,
                                         priority=SERVICE_HUB_PRIORITY,
                                         match=match,
                                         instructions=instruction)
        datapath.send_msg(flow_mod)
