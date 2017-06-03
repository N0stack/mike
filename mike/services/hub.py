from ryu.lib.packet import packet
from ryu.lib.packet import ethernet
from ryu.lib.packet import ether_types
from django.db import models

from mike.controller.openflow import MikeOpenflowController
from mike.lib.mike_object import UUIDObject
from mike.services.service import Service
from mike.lib.objects.port import Port


SERVICE_HUB_PRIORITY = 20000  # Layer 2
SERVICE_HUB_PACKET_IN_PRIORITY = 2000  # Layer 2
SERVICE_HUB_IDLE_TIMEOUT = 60


class ServiceHubTable(models.Model):
    '''
    mac address table
    {
        "id": integer,
        "hub": reference,
        "port": reference,
        "hw_addr": char[17],
        "float": boolean,
    }
    '''
    hub = models.ForeignKey(UUIDObject, editable=False, null=False)
    port = models.ForeignKey(Port, null=False, editable=False)
    hw_addr = models.CharField(max_length=17, null=False)  # ie. 1a2b3c4d5e6f
    float = models.BooleanField(default=True, null=False)

    class Meta:
        unique_together = (('port', 'hw_addr'))
        app_label = 'mike'


class Hub(Service):
    '''
    simple switching hub

    support:
      - internal to internal
      - internal to external
      - external to internal
      - internal to internal of otherport (tunneling)
    not support:
      - external to external

    task:
      - flood
      - tunneling
    '''

    def __init__(self, uuid=None):
        super(Hub, self).__init__(uuid)
        self.objects = ServiceHubTable.objects.filter(hub=self.uuid_object)

    def _update_all(self, ryu_app):
        entries = self.objects.all()
        for e in entries:
            self.learn(e.port, e.hw_addr, ryu_app, False)

    def _update_port(self, port, ryu_app):
        entries = self.objects.filter(port=port)
        for e in entries:
            self.learn(port, e.hw_addr, ryu_app, False)

    def learn(self, port, hw_addr, app, float=True):
        '''
        learning mac address
        '''
        entry = self.objects.filter(port=port)
        if entry:
            return
        new_entry = ServiceHubTable(hub=self.uuid_object,
                                    port=port,
                                    hw_addr=hw_addr,
                                    float=float)
        new_entry.save()
        flows = self._generate_flow(new_entry, app)
        for f in flows:
            ofproto = f[0].ofproto
            parser = f[0].ofproto_parser
            inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                                 f[2])]
            if float:
                flow_mod = parser.OFPFlowMod(datapath=f[0],
                                             priority=SERVICE_HUB_PRIORITY,
                                             command=ofproto.OFPFC_ADD,
                                             match=f[1],
                                             idle_timeout=SERVICE_HUB_IDLE_TIMEOUT,
                                             instructions=inst)
            else:
                flow_mod = parser.OFPFlowMod(datapath=f[0],
                                             priority=SERVICE_HUB_PRIORITY,
                                             command=ofproto.OFPFC_ADD,
                                             match=f[1],
                                             instructions=inst)
            f[0].send_msg(flow_mod)
            app.logger.info("flow added for %s" % port.name)

    def update(self, port, hw_addr, app, float=True):
        '''
        learning mac address
        '''
        entry = self.objects.filter(port=port)
        entry.hw_addr = hw_addr
        entry.float = float
        entry.save()
        flows = self._generate_flow(entry, app)
        for f in flows:
            ofproto = f[0].ofproto
            parser = f[0].ofproto_parser
            inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                                 f[2])]
            if float:
                flow_mod = parser.OFPFlowMod(datapath=f[0],
                                             priority=SERVICE_HUB_PRIORITY,
                                             command=ofproto.OFPFC_MODIFY,
                                             match=f[1],
                                             idle_timeout=SERVICE_HUB_IDLE_TIMEOUT,
                                             instructions=inst)
            else:
                flow_mod = parser.OFPFlowMod(datapath=f[0],
                                             priority=SERVICE_HUB_PRIORITY,
                                             command=ofproto.OFPFC_MODIFY,
                                             match=f[1],
                                             instructions=inst)
            f[0].send_msg(flow_mod)
            app.logger.info("flow added for %s" % port.name)

    def forget(self, port, hw_addr, app):
        '''
        deleting mac address
        '''
        entry = ServiceHubTable(hub=self.uuid_object,
                                port=port,
                                hw_addr=hw_addr)
        entry.delete()
        flows = self._generate_flow(entry, app)
        for f in flows:
            ofproto = f[0].ofproto
            parser = f[0].ofproto_parser
            inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                                 f[2])]
            flow_mod = parser.OFPFlowMod(datapath=f[0],
                                         priority=SERVICE_HUB_PRIORITY,
                                         command=ofproto.OFPFC_DELETE,
                                         match=f[1],
                                         instructions=inst)
            f[0].send_msg(flow_mod)

    def _generate_flow(self, entry, app):
        flows = []
        for s in self.uuid_object.switches.all():
            if entry.port.switch == s:
                '''
                myself
                '''
                datapath = MikeOpenflowController.get_datapath(entry.port.switch.datapath_id)
                parser = datapath.ofproto_parser
                match = parser.OFPMatch(eth_dst=entry.hw_addr)
                actions = [parser.OFPActionOutput(entry.port.number)]
                flows.append((datapath, match, actions))
            elif entry.port.switch.host_id == s.host_id:
                '''
                to external
                '''
                l = entry.port.switch.links.filter(next_link__switch=s)
                if not l:
                    entries = ServiceHubTable(hub=self.uuid_object,
                                              port__switch=s)
                    for e in entries:
                        self.forget(e.port, e.hw_addr, app)
                    # raise Exception("not linked switches in same port")
                    raise Exception('no flow for %s(%s) on %s, deleted', (s.name, s.uuid, s.port_id))  # 操作がない

                # developing
                datapath = MikeOpenflowController.get_datapath(entry.port.switch.datapath_id)
                parser = datapath.ofproto_parser
                match = parser.OFPMatch(eth_dst=entry.hw_addr)
                actions = [parser.OFPActionOutput(l.number)]
                flows.append((datapath, match, actions))
            elif entry.port.switch.host_id != s.host_id:
                '''
                to internal(tunneling)
                '''
                app.logger.info("tunnel")
        return flows

    def _generate_broadcast(self, datapath, switch):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        match = parser.OFPMatch(eth_dst='ff:ff:ff:ff:ff:ff')
        actions = []
        if switch.type == 'ex':
            for p in switch.ports.all():
                actions.append(parser.OFPActionOutput(p.number))
        else:
            actions.append(parser.OFPActionOutput(ofproto.OFPP_FLOOD))
        return (datapath, match, actions)

    def add_port(self, ev, port, app):
        datapath = ev.msg.datapath
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        flow = self._generate_broadcast(datapath, port.switch)
        i = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, flow[2])]
        mod = parser.OFPFlowMod(datapath=datapath,
                                priority=SERVICE_HUB_PRIORITY,
                                command=ofproto.OFPFC_MODIFY,
                                match=flow[1],
                                instructions=i)
        datapath.send_msg(mod)
        # TODO: flowの追加

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

    def init_ports(self, ev, switch, app):
        # delete old flows
        old_flows = self.objects.filter(port__switch__datapath_id=ev.msg.datapath.id,
                                        float=True)
        old_flows.delete()

        datapath = ev.msg.datapath
        cookie = MikeOpenflowController.add_cookie_hook(self.uuid_object.uuid)
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, actions)]
        mod = parser.OFPFlowMod(datapath=datapath,
                                priority=SERVICE_HUB_PACKET_IN_PRIORITY,
                                cookie=cookie,
                                command=ofproto.OFPFC_ADD,
                                match=match,
                                instructions=inst)
        datapath.send_msg(mod)

        flow = self._generate_broadcast(datapath, switch)
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS, flow[2])]
        mod = parser.OFPFlowMod(datapath=datapath,
                                priority=SERVICE_HUB_PRIORITY,
                                command=ofproto.OFPFC_ADD,
                                match=flow[1],
                                instructions=inst)
        datapath.send_msg(mod)

        self._update_all(app)

    def packet_in(self, ev, app):
        in_port = ev.msg.match['in_port']
        pkt = packet.Packet(ev.msg.data)
        eth = pkt.get_protocols(ethernet.ethernet)[0]
        if eth.ethertype == ether_types.ETH_TYPE_LLDP:
            return
        src_hwaddr = eth.src
        dst_hwaddr = eth.dst

        p = Port.objects.filter(number=in_port,
                                switch__datapath_id=ev.msg.datapath.id)[0]
        self.learn(p, src_hwaddr, app)

        datapath = ev.msg.datapath
        entry = self.objects.filter(hw_addr=dst_hwaddr)
        if not entry:
            return  # debug
            raise Exception('does not hub entry')
        out_port = entry[0].port.number

        # from IPython.core.debugger import Pdb
        # Pdb(color_scheme='Linux').set_trace()

        actions = [datapath.ofproto_parser.OFPActionOutput(out_port)]
        data = None
        if ev.msg.buffer_id == datapath.ofproto.OFP_NO_BUFFER:
            data = ev.msg.data
        out = datapath.ofproto_parser.OFPPacketOut(datapath=datapath,
                                                   buffer_id=ev.msg.buffer_id,
                                                   in_port=in_port,
                                                   actions=actions,
                                                   data=data)
        datapath.send_msg(out)
