# from mike.services.hub import Hub, ModelServiceHubTable
# from mike.models import ModelPort, ModelLink, ModelSwitch

# from unittest import TestCase, mock
# from nose.tools import ok_, eq_


# class TestHub(TestCase):

#     @classmethod
#     def setup_class(clazz):
#         pass
 
#     @classmethod
#     def teardown_class(clazz):
#         pass
 
#     def setup(self):
#         self.h = Hub(ryu_app=mock.MagicMock)
#         self.send_result = mock.MagicMock(return_value=0)

#         # to same internal switch
#         new_port = ModelPort()
#         new_port.save()
#         new_query = ModelServiceHubTable(hub=self.h.uuid,
#                                          port=new_port)
#         new_query.save()

#         # to external switch
#         new_switch = ModelSwitch()
#         new_port = ModelPort()
#         new_port.save()
#         new_link = ModelLink()
#         new_link.save
#         new_query = ModelServiceHubTable(hub=self.h.uuid,
#                                          port=new_port)
#         new_query.save()

#         # to other host internal switch


 
#     def teardown(self):
#         pass
 
#     class MockDatapath():
#         def __init__(self, id):
#             self.id = id
#             self.ofproto_parser.OFPMatch = mock.MagicMock(side_effect=self.mock_method)
#             self.ofproto_parser.OFPActionOutput = mock.MagicMock(side_effect=self.mock_method)
#             self.send_msg = self.send_result

#         def mock_method(self, *args, **kwargs):
#             return (args, kwargs)

#     def test_valid_add_port(self):
#         mock_port = mock.MagicMock
#         mock_port.datapath_id = 10

#         def get_datapath(app, id):
#             return self.MockDatapath(id)

#         mock.patch("mike.services.hub.get_datapath", side_effect=get_datapath)
#         with mock.patch("mike.services.hub.send_message", return_value=-1) as m:
#             self.h.add_port(port=mock_port)

#         assert len(self.send_result.call_args_list) == 3
