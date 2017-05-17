from ryu.base import app_manager
from ryu.controller import ofp_event, dpset
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from hashlib import md5

from mike.lib.objects.switch import Switch
from mike.lib.objects.port import Port
from mike.lib.objects.host import Host
from mike.lib.objects.link import Link
from mike.lib.uuid_object import get_object_type

class MikeOpenflowController(app_manager.RyuApp):
    '''
    openflow controller
    '''
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    cookies = {}
    '''
    cookies[cookie] = uuid
    cookie: 64bit => md5(uuid)
    '''

    def __init__(self, *args, **kwargs):
        super(MikeOpenflowController, self).__init__(*args, **kwargs)

    @classmethod
    def add_packet_in_hook(cls, uuid):
        '''
        return cookie hooked packet_in_handler
        '''
        cookie = md5(uuid).digest()
        cls.cookies[cookie] = uuid
        return cookie

    @staticmethod
    def _class_def(path, name):
        class_mod = __import__(path, fromlist=[name])
        return getattr(class_mod, name)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def _switch_features_handler(self, ev):
        self.logger.info("switch added: %d" % ev.msg.datapath.id)

    @set_ev_cls(ofp_event.EventOFPPortDescStatsReply, CONFIG_DISPATCHER)
    def _port_desc_stats_reply_handler(self, ev):
        switch = Switch.objects.filter(datapath_id=ev.msg.datapath.id)
        if not switch:
            # TODO: このあと、スイッチを追加した場合どうするか
            raise Exception('not registered this switch(%d)' % ev.msg.datapath.id)  # TODO: Exceptionを変える

        for s in switch[0].services.all():
            self._class_def(s.object_type.path,
                            s.object_type.type)(s.uuid).reinit_ports(ev, switch[0], self)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        # TODO: 遅延が心配
        uuid = self.cookies[ev.msg.cookie]
        object_type = get_object_type(uuid=uuid)
        self._class_def(object_type.path,
                        object_type.type)(uuid).packet_in_handler(ev, self)

    @set_ev_cls(dpset.EventPortAdd, MAIN_DISPATCHER)
    def _add_port_handler(self, ev):
        h = Host.objects.filter(switch__datapath_id=ev.dp.id,
                                name=ev.port.name)
        if h:
            h[0].number = ev.port.port_no
            h[0].mac_addr = ev.port.hw_addr  # TODO: 本当か?
            h[0].save()

            for s in h[0].switch.services.all():
                c = self._class_def(s.object_type.path,
                                    s.object_type.type)
                c(s.uuid).add_host(ev=ev,
                                   host=h[0],
                                   app=self)
            return

        l = Link.objects.filter(switch__datapath_id=ev.dp.id,
                                name=ev.port.name)
        if l:
            # check connect status
            l[0].number = ev.port.port_no
            l[0].save()

            for s in l[0].switch.services.all():
                c = self._class_def(s.object_type.path,
                                    s.object_type.type)
                c(s.uuid).add_link(ev=ev,
                                   link=l[0],
                                   app=self)
            return
        raise Exception('[add] not registered this port(%d, %s) on the switch(%d)' % (ev.port.port_no, ev.port.name, ev.dp.id))

    @set_ev_cls(dpset.EventPortDelete, MAIN_DISPATCHER)
    def _delete_port_handler(self, ev):
        h = Host.objects.filter(switch__datapath_id=ev.dp.id,
                                number=ev.port.port_no)
        if h:
            for s in h[0].switch.services.all():
                c = self._class_def(s.object_type.path,
                                    s.object_type.type)
                c(s.uuid).delete_host(ev=ev,
                                      host=h[0],
                                      app=self)
            h.delete()
            return

        l = Link.objects.filter(switch__datapath_id=ev.dp.id,
                                number=ev.port.port_no)
        if l:
            for s in l[0].switch.services.all():
                c = self._class_def(s.object_type.path,
                                    s.object_type.type)
                c(s.uuid).delete_link(ev=ev,
                                      link=l[0],
                                      app=self)
            l[0].delete()
            return

        raise Exception('[delete] not registered this port(%d, %s) on the switch(%d)' % (ev.port.port_no, ev.port.name, ev.dp.id))

    @set_ev_cls(dpset.EventPortModify, MAIN_DISPATCHER)
    def _modify_port_handler(self, ev):
        h = Host.objects.filter(switch__datapath_id=ev.dp.id,
                                number=ev.port.port_no)
        if h:
            h[0].number = ev.port.port_no
            h[0].name = ev.port.name
            h[0].mac_addr = ev.port.hw_addr  # TODO: 本当か?
            h[0].save()

            for s in h[0].switch.services.all():
                c = self._class_def(s.object_type.path,
                                    s.object_type.type)
                c(s.uuid).modify_port(ev=ev,
                                      host=h[0],
                                      app=self)
            return

        l = Link.objects.filter(switch__datapath_id=ev.dp.id,
                                number=ev.port.port_no)
        if l:
            # check connect status
            l[0].number = ev.port.port_no
            l[0].name = ev.port.name
            l[0].save()

            for s in l[0].switch.services.all():
                c = self._class_def(s.object_type.path,
                                    s.object_type.type)
                c(s.uuid).modify_link(ev=ev,
                                      link=l[0],
                                      app=self)
            return
        raise Exception('[modify] not registered this port(%d, %s) on the switch(%d)' % (ev.port.port_no, ev.port.name, ev.dp.id))
