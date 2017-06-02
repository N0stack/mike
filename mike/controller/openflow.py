from ryu.base import app_manager
from ryu.controller import ofp_event, dpset
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from hashlib import md5

from mike.lib.objects.switch import Switch
from mike.lib.objects.port import Port
from mike.lib.objects.link import Link
from mike.lib.mike_object import get_object_type


class MikeOpenflowController(app_manager.RyuApp):
    '''
    openflow controller
    '''
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(MikeOpenflowController, self).__init__(*args, **kwargs)

    _cookies = {}
    '''
    cookies[cookie] = uuid
    cookie: 64bit => md5(uuid)
    '''

    @classmethod
    def add_cookie_hook(cls, uuid):
        '''
        return cookie hooked packet_in_handler
        '''
        _cookie = md5(uuid).digest()
        cls._cookies[cookie] = uuid
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
                            s.object_type.name)(s.uuid).init_ports(ev,
                                                                   switch[0],
                                                                   self)
        for p in ev.msg.body:
            new_port = Port(switch=switch,
                            number=p.port_no,
                            name=p.name)
            try:  # TODO: check Exception, maybe uniq
                new_port.save()
                self._class_def(s.object_type.path,
                                s.object_type.name)(s.uuid).add_port(ev,
                                                                     new_port,
                                                                     self)
            except:
                pass

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, ev):
        # TODO: 遅延が心配
        uuid = self._cookies[ev.msg.cookie]
        object_type = get_object_type(uuid=uuid)
        self._class_def(object_type.path,
                        object_type.name)(uuid).packet_in(ev, self)

    @set_ev_cls(dpset.EventPortAdd, MAIN_DISPATCHER)
    def _add_port_handler(self, ev):
        l = Link.objects.filter(switch__datapath_id=ev.dp.id,
                                name=ev.port.name)
        if l:
            # TODO: check connect status
            l[0].number = ev.port.port_no
            l[0].save()

            for s in l[0].switch.services.all():
                c = self._class_def(s.object_type.path,
                                    s.object_type.name)
                c(s.uuid).add_link(ev=ev,
                                   link=l[0],
                                   app=self)
            return

        sw = Switch.objects.filter(datapath_id=ev.dp.id)[0]
        p = Port(switch=sw,
                 number=ev.port.port_no,
                 name=ev.port.name)
        p.save()
        for s in sw.services.all():
            c = self._class_def(s.object_type.path,
                                s.object_type.name)
            c(s.uuid).add_port(ev=ev,
                               port=p,
                               app=self)

    @set_ev_cls(dpset.EventPortDelete, MAIN_DISPATCHER)
    def _delete_port_handler(self, ev):
        p = Port.objects.filter(switch__datapath_id=ev.dp.id,
                                number=ev.port.port_no)
        if p:
            for s in p[0].switch.services.all():
                c = self._class_def(s.object_type.path,
                                    s.object_type.name)
                c(s.uuid).delete_port(ev=ev,
                                      port=p[0],
                                      app=self)
            p[0].delete()
            return

        l = Link.objects.filter(switch__datapath_id=ev.dp.id,
                                number=ev.port.port_no)
        if l:
            for s in l[0].switch.services.all():
                c = self._class_def(s.object_type.path,
                                    s.object_type.name)
                c(s.uuid).delete_link(ev=ev,
                                      link=l[0],
                                      app=self)
            l[0].delete()
            return

        raise Exception('[delete] not registered this port(%d, %s) on the switch(%d)' % (ev.port.port_no, ev.port.name, ev.dp.id))

    @set_ev_cls(dpset.EventPortModify, MAIN_DISPATCHER)
    def _modify_port_handler(self, ev):
        p = Port.objects.filter(switch__datapath_id=ev.dp.id,
                                number=ev.port.port_no)
        if p:
            p[0].number = ev.port.port_no
            p[0].name = ev.port.name
            p[0].save()

            for s in p[0].switch.services.all():
                c = self._class_def(s.object_type.path,
                                    s.object_type.name)
                c(s.uuid).modify_port(ev=ev,
                                      port=p[0],
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
                                    s.object_type.name)
                c(s.uuid).modify_link(ev=ev,
                                      link=l[0],
                                      app=self)
            return
        raise Exception('[modify] not registered this port(%d, %s) on the switch(%d)' % (ev.port.port_no, ev.port.name, ev.dp.id))
