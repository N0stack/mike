from mike.lib.objects.switches import Switches

from unittest import TestCase, mock
from uuid import uuid4


class TestHub(TestCase):

    @classmethod
    def setup_class(clazz):
        pass
 
    @classmethod
    def teardown_class(clazz):
        pass
 
    def setup(self):
        pass
 
    def teardown(self):
        pass
 
    def test_switch(self):
        host_id = uuid4()

        uuids = []
        uuids[0] = Switches.add(name="test_sw1",
                                host_id=host_id,
                                datapath_id=1)
        r = Switches.get_from_uuids(uuids)[0]
        assert r.name == "test_sw1"
        assert r.host_id == host_id
        assert r.internal
        assert r.datapath_id == 1

        uuids[1] = Switches.add(name="test_sw2",
                                host_id=host_id,
                                internal=False,
                                datapath_id=2)
        Switches.delete([uuids[0]])

        r = Switches.get_from_uuids(uuids)[0]
        assert r.name == "test_sw2"
        assert r.host_id == host_id
        assert not r.internal
        assert r.datapath_id == 2

    # @exception
    def test_add_exists_switch(self):
        pass
