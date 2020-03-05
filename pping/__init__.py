ABOUT = {
    'name': 'pping',
    'version': '0.0.6',
    'author': 'JLMin',
    'description': 'ping in python',
    'url': 'https://github.com/JLMin/pping',
    'license': 'MIT'
}


def ping(address, **kwargs):
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
