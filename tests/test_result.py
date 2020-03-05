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
            ('127.0.0.1',
             [Response._timeout(),
              Response._Valid(Response.OK, '1.2.3.4', '5.6.7.8', 32,
                              2, 1, 0.1)]),
        )
    )
    def test_result_timed_out(self, addr, resps):
        result = Result(addr, resps)
        assert result.hostname
        assert result.hostalias == []
        assert result.iplist == ['127.0.0.1']
        assert result[0].status == Response.TIMEDOUT
        assert 'statistics' in str(result)
        assert 'Request timed out.' in str(result)
        assert 'L:1' in repr(result)

    @pytest.mark.parametrize(
        'addr, resps', (
            ('127.0.0.1',
             [Response._Valid(Response.OK, '1.2.3.4', '5.6.7.8', 32,
                              2, 1, 0.1),
              Response._Valid(Response.OK, '1.2.3.4', '5.6.7.8', 32,
                              2, 2, 0.1)]),
        )
    )
    def test_result_no_error(self, addr, resps):
        result = Result(addr, resps)
        assert result.hostname
        assert result.hostalias == []
        assert result.iplist == ['127.0.0.1']
        assert result[0].status == Response.OK
        assert 'statistics' in str(result)
        assert 'Request timed out.' not in str(result)
        assert 'L:0' in repr(result)
