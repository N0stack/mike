from mike.objects.switches import Switches

from ryu.base import app_manager
from ryu.controller import ofp_event
from ryu.controller.handler import CONFIG_DISPATCHER, MAIN_DISPATCHER
from ryu.controller.handler import set_ev_cls
from ryu.ofproto import ofproto_v1_3


class MikeOpenflowController(app_manager.RyuApp):
    OFP_VERSIONS = [ofproto_v1_3.OFP_VERSION]

    def __init__(self, *args, **kwargs):
        super(MikeOpenflowController, self).__init__(*args, **kwargs)

    @set_ev_cls(ofp_event.EventOFPSwitchFeatures, CONFIG_DISPATCHER)
    def switch_features_handler(self, event):
        datapath = event.msg.datapath
        switch = Switches.models.objects.filter(datapath_id=datapath.id)[0]
        if not switch:
            # 追加したあと、スイッチを追加した場合どうするか
            raise  # 'not registered this switch(%d)' % datapath.id
        if switch.type is 'in':
            return

        # external of physical switch has packet in handller
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser
        match = parser.OFPMatch()
        actions = [parser.OFPActionOutput(ofproto.OFPP_CONTROLLER,
                                          ofproto.OFPCML_NO_BUFFER)]
        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        datapath.send_msg(parser.OFPFlowMod(datapath=datapath, priority=0,
                                            match=match, instructions=inst))

    @set_ev_cls(ofp_event.EventOFPPacketIn, MAIN_DISPATCHER)
    def _packet_in_handler(self, event):
        pass

    # @set_ev_cls(ofp_event.EventOFPStateChange, MAIN_DISPATCHER)
    # @set_ev_cls(ofp_event.EventOFPPortStateChange, MAIN_DISPATCHER)
