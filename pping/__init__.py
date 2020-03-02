# -*- coding: utf-8 -*-


ABOUT = {
    'name': 'pping',
    'version': '0.0.4',
    'author': 'JLMin',
    'description': 'ping in python',
    'url': 'https://github.com/JLMin/pping',
    'license': 'MIT'
}


def ping(address, **kwargs):
    from .session import Request
    from .result import Result
    from .exceptions import (_raise_if_not_int_positive,
                             _raise_if_not_int_positive_or_zero,
                             _raise_if_not_num_positive,
                             _raise_if_not_num_positive_or_zero)

    # int > 0
    repeat = kwargs.get('repeat', 4)
    _raise_if_not_int_positive('repeat', repeat)

    # int | float >= 0
    interval = kwargs.get('interval', 1)
    _raise_if_not_num_positive_or_zero('interval', interval)

    # int >= 0
    size = kwargs.get('size', 32)
    _raise_if_not_int_positive_or_zero('size', size)

    # int | float > 0
    timeout = kwargs.get('timeout', 1)
    _raise_if_not_num_positive('timeout', timeout)

    # int > 0
    ttl = kwargs.get('ttl', 128)
    _raise_if_not_int_positive('ttl', ttl)

    responses = Request.ping(address=address,
                             repeat=repeat,
                             interval=interval,
                             size=size,
                             timeout=timeout,
                             ttl=ttl)
    if responses:
        return Result(address, responses)
