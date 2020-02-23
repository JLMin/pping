from pyping.ping import ping
from pyping.util import result_to_dict


def my_ping(address):
    result = ping(address, data='data')
    d_result = result_to_dict(result)

    if 'error' in d_result:
        msg = (
            'ping >> [{addr}] -> {error}'
        ).format(addr=address, **d_result)
    else:
        msg = (
            'ping >> [{src}] -> bytes={len} time={time}ms TTL={ttl}'
        ).format(**d_result)

    print(msg)


if __name__ == '__main__':
    address1 = '127.0.0.1'
    address2 = '999.0.0.0'
    my_ping(address1)
    my_ping(address2)
