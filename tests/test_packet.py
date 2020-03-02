import pytest

from pping.packet import Icmp, IPv4


class TestPacket:

    @pytest.mark.parametrize(
        'id_, seq, size', (
            (1, 4, 0),
            (2, 5, 11),
            (3, 6, 16)
        )
    )
    def test_icmp_unpack_get_same_id_seq_and_size(self, id_, seq, size):
        packet = Icmp.pack(id_=id_, seq=seq, size=size)
        unpack = Icmp.unpack(packet)
        assert unpack.id == id_
        assert unpack.seq == seq
        assert len(unpack.payload) == size

    @pytest.mark.parametrize(
        'src, dst, ttl', (
            ('1.2.3.4', '5.6.7.8', 0),
            ('99.99.99.99', '66.66.66.66', 64),
            ('123.123.123.123', '123.123.123.123', 33)
        )
    )
    def test_ipv4_unpack_get_same_src_dst_and_ttl(self, src, dst, ttl):
        packet = IPv4.pack(src=src, dst=dst, ttl=ttl)
        unpack = IPv4.unpack(packet)
        assert unpack.src == src
        assert unpack.dst == dst
        assert unpack.ttl == ttl
