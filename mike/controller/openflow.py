from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3
from hashlib import md5

from mike.lib.objects.switches import Switches
from mike.lib.uuid_objects import get_object_type


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
        cls.cookies[md5(uuid).digest()] = uuid

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def _switch_features_handler(self, event):
        datapath = event.msg.datapath
        switch = Switches.models.objects.filter(datapath_id=datapath.id)[0]
        if not switch:
            # TODO: このあと、スイッチを追加した場合どうするか
            raise  # 'not registered this switch(%d)' % datapath.id

        for s in switch.services.all():
            service_name, service_path = s.object_type.name, s.object_type.type
            class_mod = __import__(service_path, fromlist=[service_name])
            class_def = getattr(class_mod, service_name)
            class_def(s.uuid).switch_features_handler(event)

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, event):
        # TODO: 遅延が心配
        uuid = self.cookies[event.msg.cookie]
        object_type = get_object_type(uuid=uuid)
        service_name, service_path = object_type.name, object_type.path
        class_mod = __import__(service_path, fromlist=[service_name])
        class_def = getattr(class_mod, service_name)
        class_def(uuid).packet_in_handler(event)

    # @set_ev_cls(ofp_event.EventOFPStateChange, MAIN_DISPATCHER)
    # @set_ev_cls(ofp_event.EventOFPPortStateChange, MAIN_DISPATCHER)
