from unittest import TestCase
from nose.tools import eq_, ok_, raises
from django.db.utils import IntegrityError
from uuid import uuid4

from mike.


class TestSwitches(TestCase):
    def test_switches(self):
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
        eq_(len(Switches.get_from_uuids(uuids)), 1)

        r = Switches.get_from_uuids(uuids)[0]
        eq_(r.name, "test_sw2")
        eq_(r.host_id, host_id)
        ok_(not r.internal)
        eq_(r.datapath_id, 2)

    @raises(IntegrityError)
    def test_add_exists_switches(self):
        host_id = uuid4()

        uuids = []
        uuids.append(Switches.add(name="test_sw1",
                                  host_id=host_id,
                                  datapath_id=1))
        uuids.append(Switches.add(name="test_sw1",
                                  host_id=host_id,
                                  datapath_id=1))


class TestPorts(TestCase):
    def setUp(self):
        self.host_id = uuid4()
        self.switch_uuid = Switches.add(name="test_sw1",
                                        host_id=self.host_id,
                                        datapath_id=1)
        self.switch = Switches.get_from_uuids([self.switch_uuid])[0]

    def test_ports(self):
        ports_uuids = []

        # no name port
        ports_uuids.append(Ports.add(number=1,
                                     switch=self.switch,
                                     mac_addr="10:00:00:00:00:01"))
        # no ip address port
        ports_uuids.append(Ports.add(number=2,
                                     name="veth0",
                                     switch=self.switch,
                                     mac_addr="10:00:00:00:00:02"))
        # same mac address port
        ports_uuids.append(Ports.add(number=3,
                                     name="veth1",
                                     switch=self.switch,
                                     mac_addr="10:00:00:00:00:02"))
        # ip address port
        ports_uuids.append(Ports.add(number=4,
                                     name="veth2",
                                     switch=self.switch,
                                     mac_addr="10:00:00:00:00:03",
                                     ipv4_addr="192.168.0.1",
                                     ipv4_subnetmask="255.255.255.0"))
        # same ip address port
        ports_uuids.append(Ports.add(number=5,
                                     name="veth3",
                                     switch=self.switch,
                                     mac_addr="10:00:00:00:00:04",
                                     ipv4_addr="192.168.0.1",
                                     ipv4_subnetmask="255.255.255.0"))
        sw2_uuid = Switches.add(name="test_sw2",
                                host_id=self.host_id,
                                datapath_id=21)
        sw2 = Switches.get_from_uuids([sw2_uuid])[0]
        # othter switch same config
        ports_uuids.append(Ports.add(number=5,
                                     name="veth3",
                                     switch=sw2,
                                     mac_addr="10:00:00:00:00:04",
                                     ipv4_addr="192.168.0.1",
                                     ipv4_subnetmask="255.255.255.0"))

        p = Ports.get_from_uuids([ports_uuids[0]])[0]
        eq_(p.number, 1)
        eq_(p.name, "")
        eq_(p.switch, self.switch)
        eq_(p.mac_addr, "10:00:00:00:00:01")
        eq_(p.ipv4_addr, "")
        eq_(p.ipv4_subnetmask, "")
        p = Ports.get_from_uuids([ports_uuids[1]])[0]
        eq_(p.number, 2)
        eq_(p.name, "veth0")
        eq_(p.switch, self.switch)
        eq_(p.mac_addr, "10:00:00:00:00:02")
        eq_(p.ipv4_addr, "")
        eq_(p.ipv4_subnetmask, "")
        p = Ports.get_from_uuids([ports_uuids[2]])[0]
        eq_(p.number, 3)
        eq_(p.name, "veth1")
        eq_(p.switch, self.switch)
        eq_(p.mac_addr, "10:00:00:00:00:02")
        eq_(p.ipv4_addr, "")
        eq_(p.ipv4_subnetmask, "")
        p = Ports.get_from_uuids([ports_uuids[3]])[0]
        eq_(p.number, 4)
        eq_(p.name, "veth2")
        eq_(p.switch, self.switch)
        eq_(p.mac_addr, "10:00:00:00:00:03")
        eq_(p.ipv4_addr, "192.168.0.1")
        eq_(p.ipv4_subnetmask, "255.255.255.0")
        p = Ports.get_from_uuids([ports_uuids[4]])[0]
        eq_(p.number, 5)
        eq_(p.name, "veth3")
        eq_(p.switch, self.switch)
        eq_(p.mac_addr, "10:00:00:00:00:04")
        eq_(p.ipv4_addr, "192.168.0.1")
        eq_(p.ipv4_subnetmask, "255.255.255.0")
        p = Ports.get_from_uuids([ports_uuids[5]])[0]
        eq_(p.number, 5)
        eq_(p.name, "veth3")
        eq_(p.switch, sw2)
        eq_(p.mac_addr, "10:00:00:00:00:04")
        eq_(p.ipv4_addr, "192.168.0.1")
        eq_(p.ipv4_subnetmask, "255.255.255.0")

        # __unicode__ との比較がうまく行かないので迷う
        # eq_(p, ports_uuids[5])

        eq_(len(Ports.get_from_uuids(ports_uuids)), 6)
        del_p = Ports.model.objects.filter(switch=self.switch)
        eq_(len(del_p), 5)
        Ports.delete(del_p)
        eq_(len(Ports.get_from_uuids(ports_uuids)), 1)

    @raises(IntegrityError)
    def test_add_exists_ports(self):
        Ports.add(number=1,
                  switch=self.switch,
                  mac_addr="10:00:00:00:00:01")
        Ports.add(number=1,
                  switch=self.switch,
                  mac_addr="10:00:00:00:00:01")

    @raises(Exception)
    def test_add_ports_invalid_args(self):
        Ports.add(number=1,
                  name="veth1",
                  switch=self.switch,
                  mac_addr="10:00:00:00:00:01",
                  ipv4_addr="192.168.0.1")

    @raises(Exception)
    def test_add_ports_invalid_args_no_name(self):
        Ports.add(number=1,
                  switch=self.switch,
                  mac_addr="10:00:00:00:00:01",
                  ipv4_addr="192.168.0.1")

    @raises(Exception)
    def test_add_ports_invalid_args_subnet(self):
        Ports.add(number=1,
                  name="veth1",
                  switch=self.switch,
                  mac_addr="10:00:00:00:00:01",
                  ipv4_subnetmask="255.255.255.0")

    @raises(Exception)
    def test_add_ports_invalid_args_no_name_subnet(self):
        Ports.add(number=1,
                  switch=self.switch,
                  mac_addr="10:00:00:00:00:01",
                  ipv4_subnetmask="255.255.255.0")
