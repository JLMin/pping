import sys
import time
import concurrent.futures
import threading

from pyping.ping import ping
from pyping.util import results_statistics


SERVERS = [
    # test server
    ('badserver1', '0.0.0.0'),
    ('badserver2', '0.0.0.1'),
    ('badserver3', '0.0.0.256'),
    ('localhost1', 'localhost'),
    ('localhost2', '127.0.0.1'),

    # real server
    ('Google', 'www.google.com'),
    ('Baidu', 'www.baidu.com')
]


def ping_servers(repeat):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        futures = [executor.submit(ping_thread, s, repeat) for s in SERVERS]
        for f in futures:
            print(f.result())


def ping_thread(server, repeat):
    results = list()
    id_ = threading.get_ident()
    for i in range(repeat):
        result = ping(server[1], id_, i + 1, 'test')
        results.append(result)
        time.sleep(1)
    return stats_string(server[0], results)


def stats_string(server_name, results):
    stats = results_statistics(results)
    sent = stats['sent']
    recv = stats['recv']
    # header
    str_header = f'ping >> {server_name:<10}'
    # packet
    w = len(str(sent))
    dots = '.' * (w * 2 + 1)
    packet_all = f' [{dots}]'
    packet_bad = f' [{recv:>{w}}/{sent}]'
    str_packet = packet_all if recv == sent else packet_bad
    # time or error
    times = u' -> {avg:>3}ms ~ {std:>4}  ↑ {min:>3}ms  ↓ {max:>3}ms'
    error = u' -> {error}'
    str_body = error if 'error' in stats else times
    # ----
    full_str = str_header + str_packet + str_body.format(**stats)
    return full_str


def user_input(msg):
    try:
        command = input(msg)
        repeat = int(command)
        assert repeat > 0
    except KeyboardInterrupt:
        sys.exit()
    except (ValueError, AssertionError):
        return 0
    else:
        return repeat


def run_script():
    while True:
        repeat = user_input('How many pings you want to send?\n> ')
        if repeat:
            start_time = time.time()
            ping_servers(repeat)
            time_cost = time.time() - start_time
            # summary
            print(
                f'{"-" * 60}\n'
                f'[{repeat}] ping request(s) were sent to each server.\n'
                f'Finished in: {round(time_cost, 3)} Seconds.\n'
            )
        else:
            break


if __name__ == '__main__':
    run_script()
