from mike.lib.objects.switches import Switches

from nose.tools import eq_, ok_, raises
from django.db.utils import IntegrityError
from uuid import uuid4


def test_switches():
    host_id = uuid4()

    uuids = []
    uuids.append(Switches.add(name="test_sw1",
                              host_id=host_id,
                              datapath_id=1))
    r = Switches.get_from_uuids(uuids)[0]
    eq_(r.name, "test_sw1")
    eq_(r.host_id, host_id)
    ok_(r.internal)
    eq_(r.datapath_id, 1)

    uuids.append(Switches.add(name="test_sw2",
                              host_id=host_id,
                              internal=False,
                              datapath_id=2))
    eq_(len(Switches.get_from_uuids(uuids)), 2)
    Switches.delete([uuids[0]])

    r = Switches.get_from_uuids(uuids)[0]
    eq_(r.name, "test_sw2")
    eq_(r.host_id, host_id)
    ok_(not r.internal)
    eq_(r.datapath_id, 2)


@raises(IntegrityError)
def test_add_exists_switches():
    host_id = uuid4()

    uuids = []
    uuids.append(Switches.add(name="test_sw1",
                              host_id=host_id,
                              datapath_id=1))
    uuids.append(Switches.add(name="test_sw1",
                              host_id=host_id,
                              datapath_id=1))
