from ryu.app.ofctl.api import get_datapath
from django.db import models

from mike.services.service import Service
from mike.lib.objects.switch import Switch
from mike.lib.objects.link import Link
from mike.lib.objects.host import Host


SERVICE_HUB_PRIORITY = 20000  # Layer 2


class ServiceHubTable(models.Model):
    hub = models.UUIDField(editable=False, null=False)
    host = models.ForeignKey(Host, null=False)

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

    def __init__(self, uuid=None):
        super(Hub, self).__init__(uuid)

    def _learn_all(self, ryu_app):
        hosts = Host.objects.filter(switch__in=self.uuid_object.switches)
        for h in hosts:
            self._learn(h, ryu_app)

    def _learn(self, host, ryu_app):
        '''
        learning mac address
        '''
        new_network = ServiceHubTable(hub=self.uuid_object, host=host)
        new_network.save()
        flows = self._generate_flow(host, ryu_app)
        for f in flows:
            ofproto = f[0].ofproto
            parser = f[0].ofproto_parser
            inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,  # TODO: UPDATEに変更する
                                                 f[2])]
            flow_mod = parser.OFPFlowMod(datapath=f[0],
                                         priority=SERVICE_HUB_PRIORITY,
                                         match=f[1],
                                         instructions=inst)
            f[0].send_msg(flow_mod)

    def _forget(self, host, ryu_app):
        '''
        deleting mac address
        '''
        new_network = ServiceHubTable(hub=self.uuid_object, host=host)
        new_network.delete()
        flows = self._generate_flow(host, ryu_app)
        for f in flows:
            ofproto = f[0].ofproto
            parser = f[0].ofproto_parser
            inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,  # TODO: DELETEに変更する
                                                 f[2])]
            flow_mod = parser.OFPFlowMod(datapath=f[0],
                                         priority=SERVICE_HUB_PRIORITY,
                                         match=f[1],
                                         instructions=inst)
            f[0].send_msg(flow_mod)

    def generate_flow(self, host, ryu_app):
        flows = []
        for s in self.uuid_object.switches.all():
            if host.switch is s:
                '''
                myself
                '''
                datapath = get_datapath(ryu_app,
                                        host.switch.datapath_id)
                parser = datapath.ofproto_parser
                match = parser.OFPMatch(eth_dst=host.hw_addr)
                actions = [parser.OFPActionOutput(host.number)]
                flows.append((datapath, match, actions))
            elif host.switch.host_id == s.host_id:
                '''
                to external
                '''
                l = host.switch.links.filter(next_link__switch=s)
                if not l:
                    hosts = Host.objects.filter(switch=s)
                    for h in hosts:
                        self._forget(h, ryu_app)
                    # raise Exception("not linked switches in same host")
                    raise Exception('no flow for %s(%s) on %s, deleted', (s.name, s.uuid, s.host_id))  # 操作がない

                datapath = get_datapath(ryu_app,
                                        host.switch.datapath_id)
                parser = datapath.ofproto_parser
                match = parser.OFPMatch(eth_dst=host.hw_addr)
                actions = [parser.OFPActionOutput(l.number)]
                flows.append((datapath, match, actions))
            elif host.switch.host_id != s.host_id:
                '''
                to internal(tunneling)
                '''
                pass

    def add_host(self, ev, host, app):
        self._learn(host, app)

    def delete_host(self, ev, host, app):
        self._forget(host, app)

    def modify_host(self, ev, host, app):
        self._learn(host, app)

    def add_link(self, ev, link, app):
        self._learn_all(app)

    def delete_link(self, ev, link, app):
        self._learn_all(app)

    def modify_link(self, ev, link, app):
        self._learn_all(app)

    def reinit_ports(self, ev, switch, app):
        self._learn_all(app)
