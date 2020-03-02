import pytest

from pping import ping
from pping.result import Result


class TestApi:

    @pytest.mark.parametrize(
        'repeat, interval, size, timeout, ttl', (
            # valid input default:
            # (4, 1, 32, 1, 128)

            # repeat : int > 0
            ('4', 1, 32, 1, 128),   # str
            (0, 1, 32, 1, 128),     # zero
            (1.0, 1, 32, 1, 128),   # float
            (-1, 1, 32, 1, 128),    # negative
            (True, 1, 32, 1, 128),  # boolean

            # interval : int | float >= 0
            (4, '1', 32, 1, 128),   # str
            (4, -0.2, 32, 1, 128),  # negative
            (4, True, 32, 1, 128),  # boolean

            # size : int >= 0
            (4, 1, '32', 1, 128),   # str
            (4, 1, 1.2, 1, 128),    # float
            (4, 1, -2, 1, 128),     # negative
            (4, 1, True, 1, 128),   # boolean

            # timeout : int | float > 0
            (4, 1, 32, '1', 128),   # str
            (4, 1, 32, 0, 128),     # zero
            (4, 1, 32, -1, 128),    # negative
            (4, 1, 32, True, 128),  # boolean

            # ttl : int > 0
            (4, 1, 32, 1, '128'),   # str
            (4, 1, 32, 1, 0),       # zero
            (4, 1, 32, 1, 2.5),     # float
            (4, 1, 32, 1, -2),      # negative
            (4, 1, 32, 1, True),    # boolean
        )
    )
    def test_invalid_input(self, repeat, interval, size, timeout, ttl):
        with pytest.raises(ValueError):
            ping(address='8.8.8.8',
                 repeat=repeat,
                 interval=interval,
                 size=size,
                 timeout=timeout,
                 ttl=ttl)

    def test_valid_input(self):
        repeat = 4
        result = ping(address='localhost',
                      repeat=repeat,
                      interval=0.2,
                      size=0,
                      timeout=1,
                      ttl=32)
        assert isinstance(result, Result)
        assert result.sent == repeat
        assert result.recv == repeat
        assert result.lost == 0
