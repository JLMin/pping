ABOUT = {
    'name': 'pping',
    'version': '0.0.8',
    'author': 'JLMin',
    'description': 'ping in python',
    'url': 'https://github.com/JLMin/pping',
    'license': 'MIT'
}


def ping(address, **kwargs):
    """Send a ping request to the target address, returns the result.

    :param address: str           Host name or IPv4 address.
    :param repeat: int            Number of echo requests to send.
    :param interval: int | float  Time in seconds interval between each request.
    :param size: int              Send buffer size in bytes.
    :param timeout: int | float   Timeout in seconds to wait for each reply.
    :param ttl: int               Time To Live.

    :return: :class:`Result` object

    Usage::
      >>> from pping import ping
      >>> result = ping('example.com')
      >>> result
      Result of [example.com] > 168ms ~ 2.2 [4/4, L:0]
    """

    from .session import Request
    from .result import Result
    from .utils import verify_args

    repeat = kwargs.get('repeat', 4)
    verify_args(arg=repeat, name='repeat', type_='integer', value='>0')

    interval = kwargs.get('interval', 1)
    verify_args(arg=interval, name='interval', type_='number', value='>=0')

    size = kwargs.get('size', 32)
    verify_args(arg=size, name='size', type_='integer', value='>=0')

    timeout = kwargs.get('timeout', 1)
    verify_args(arg=timeout, name='timeout', type_='number', value='>0')

    ttl = kwargs.get('ttl', 128)
    verify_args(arg=ttl, name='ttl', type_='integer', value='>0')

    responses = Request.ping(address=address,
                             repeat=repeat,
                             interval=interval,
                             size=size,
                             timeout=timeout,
                             ttl=ttl)
    return Result(address, responses)
