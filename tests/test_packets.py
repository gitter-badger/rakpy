# -*- coding: utf-8 -*-
import pytest

from rakpy.protocol import decode_packet
from rakpy.protocol.packets import Packet, UnconnectedPing


def test_packet_id():

    class DummyPacket(Packet):
        class Meta:
            id = 0x42
            structure = ()

    packet = DummyPacket()

    # setter
    with pytest.raises(AttributeError):
        packet.id = 0xff

    # getter
    assert packet.id == 0x42


def test_unconnected_ping():

    # invalid packet id
    with pytest.raises(ValueError):
        UnconnectedPing("\x42\x00\x00\x00\x00")

    data = "\x01\x00\x00\x00\x00\x00\x02\xf3\x47\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78\x00\x05\x27\x00\xaa\x0a\x23\xa3"
    packet = UnconnectedPing(data)
    assert packet.ping_id == 193351
    assert packet.client_id == 1450258689827747
    assert unicode(packet) == "UnconnectedPing(ping_id=193351, client_id=1450258689827747)"


def test_decode_packet():
    data = "\x01\x00\x00\x00\x00\x00\x02\xf3\x47\x00\xff\xff\x00\xfe\xfe\xfe\xfe\xfd\xfd\xfd\xfd\x12\x34\x56\x78\x00\x05\x27\x00\xaa\x0a\x23\xa3"
    packet = decode_packet(data)
    assert packet.id == 0x01
    assert type(packet) == UnconnectedPing
