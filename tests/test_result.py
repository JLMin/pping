import pytest

from pping.result import Result
from pping.packet import Icmp, IPv4
from pping.session import Response


class TestPacket:

    @pytest.mark.parametrize(
        'addr, resps', (
            ('-1.0.0.0', [Response._error('error')]),
            ('256.0.0.0', [Response._error('error')]),
        )
    )
    def test_result_with_error(self, addr, resps):
        result = Result(addr, resps)
        assert result.hostname
        assert result.hostalias == []
        assert result.iplist == []
        assert result[0].status == Response.ERROR
        assert 'error' in str(result)
        assert 'error' in repr(result)

    @pytest.mark.parametrize(
        'addr, resps', (
            ('random.jmsjms.com', [Response._timeout()]),
        )
    )
    def test_result_all_timed_out(self, addr, resps):
        result = Result(addr, resps)
        assert result.hostname
        assert result.hostalias
        assert result.iplist
        assert result[0].status == Response.TIMEDOUT
        assert 'Request timed out.' in str(result)
        assert 'error' in repr(result)

    def test_result_no_error(self):
        addr = '127.0.0.1'
        ip_pk = IPv4.pack(src=addr, dst=addr, ttl=32)
        ic_pk = Icmp.pack(id_=1, seq=1, size=0)
        packet = ip_pk + ic_pk
        resps = [Response._valid(packet=packet, rtt=0.1)]

        result = Result(addr, resps)
        assert result.hostname
        assert result.hostalias == []
        assert result.iplist == ['127.0.0.1']
        assert result[0].status == Response.OK
        assert 'statistics' in str(result)
        assert 'error' not in repr(result)
