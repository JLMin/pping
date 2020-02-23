from collections import namedtuple
import concurrent.futures
import threading
import time

from pyping.ping import ping
from pyping.util import results_statistics


Server = namedtuple('Server', ['name', 'address'])
SERVERS = [
    # test server
    Server('badserver1', '0.0.0.0'),
    Server('badserver2', '0.0.0.1'),
    Server('badserver3', '0.0.0.256'),
    Server('localhost1', 'localhost'),
    Server('localhost2', '127.0.0.1'),
    # real server
    Server('Google', 'www.google.com'),
    Server('Baidu', 'www.baidu.com')
]


def ping_servers(repeat):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(ping_thread, s, repeat) for s in SERVERS]
    return [f.result() for f in futures]


def ping_thread(server, repeat):
    results = list()
    id_ = threading.get_ident()
    for i in range(repeat):
        result = ping(address=server.address, id_=id_, seq=i + 1, data='data')
        results.append(result)
        time.sleep(1)
    return stats_string(server.name, results)


def stats_string(server_name, results):
    stats = results_statistics(results)
    # header
    str_header = f' {server_name:<10}'
    # packet
    lpct = stats['lpct']
    recv = '·' * int((1 - lpct) * 10)
    str_packet = f' [{recv:<10}]'
    # time or error
    times = ' -> {avg:>3}ms ~ {std:>4}  ↑ {min:>3}ms  ↓ {max:>3}ms'
    error = ' -> {error}'
    str_body = error if 'error' in stats else times
    # ----
    full_str = str_header + str_packet + str_body.format(**stats)
    return full_str


def execute(repeat):
    start_time = time.time()
    results = ping_servers(repeat)
    time_cost = time.time() - start_time
    # summary
    print()
    print(*results, sep='\n')
    total = f'{repeat} ping request(s) were sent to each server'
    tcost = f'total time cost: {round(time_cost, 3)} seconds'
    print(f'{"-" * 59}\n{total:>58}\n{tcost:>58}\n')


def user_input(msg):
    while True:
        command = input(msg)
        try:
            repeat = int(command)
            assert repeat > 0
        except (ValueError, AssertionError):
            break
        else:
            execute(repeat)


if __name__ == "__main__":
    msg = 'How many pings you want to send?\n> '
    user_input(msg)
