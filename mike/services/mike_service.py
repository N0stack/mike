from abc import ABCMeta, abstractmethod


class MikeService(metaclass=ABCMeta):
    def __init__(self, *args, **kwargs):
        pass

    def packet_in(self):
        pass

    '''
    add new flow for switch
    load protocol data
    '''
    @abstractmethod
    def add_flow(self):
        pass

    def _send_flow(self, datapath, priority, match, actions, buffer_id=None):
        ofproto = datapath.ofproto
        parser = datapath.ofproto_parser

        inst = [parser.OFPInstructionActions(ofproto.OFPIT_APPLY_ACTIONS,
                                             actions)]
        if buffer_id:
            mod = parser.OFPFlowMod(datapath=datapath, buffer_id=buffer_id,
                                    priority=priority, match=match,
                                    instructions=inst)
        else:
            mod = parser.OFPFlowMod(datapath=datapath, priority=priority,
                                    match=match, instructions=inst)
        datapath.send_msg(mod)
