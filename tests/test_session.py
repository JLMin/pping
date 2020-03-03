import pytest

from pping.session import Request, Response


class TestSession:

    @pytest.mark.parametrize(
        'address', (
            '-1.0.0.0',
            '256.0.0.0',
            '?'
        )
    )
    def test_ping_returns_only_one_result_with_invalid_address(self, address):
        # repeat > 1, assert len(result) == 1
        result = Request.ping(address=address, repeat=4, interval=1,
                              size=0, timeout=1, ttl=64)
        assert isinstance(result, list)
        assert len(result) == 1
        assert result[0].status == Response.ERROR

    @pytest.mark.parametrize(
        'address, repeat, timeout', (
            ('127.0.0.1', 2, 0.5),
        )
    )
    def test_reliable_address(self, address, repeat, timeout):
        result = Request.ping(address=address, repeat=repeat, interval=0,
                              size=32, timeout=timeout, ttl=64)
        assert isinstance(result, list)
        assert len(result) == repeat
        assert result[0].status == Response.OK

    @pytest.mark.parametrize(
        'address, repeat, timeout', (
            ('random.jmsjms.com', 2, 0.2),
        )
    )
    def test_timed_out(self, address, repeat, timeout):
        # this is a ping-able address for real, but
        # I'm pretty sure we can't receive reply from this it.
        # If somehow you can get reply from it, this test will fail.
        result = Request.ping(address=address, repeat=repeat, interval=0,
                              size=32, timeout=timeout, ttl=64)
        assert isinstance(result, list)
        assert len(result) == repeat
        assert result[0].status == Response.TIMEDOUT
