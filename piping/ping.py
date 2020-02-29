# -*- coding: utf-8 -*-

import sys
import select
import socket
import threading
import time

from .packet import Icmp
from .result import Response, Result
from .exceptions import (_int_positive, _int_positive_or_zero,
                         _num_positive, _num_positive_or_zero)


def ping(address, repeat=4, interval=1, size=32, timeout=1, ttl=128):
    # verify args
    _int_positive('repeat', repeat)
    _num_positive_or_zero('interval', interval)
    _int_positive_or_zero('size', size)
    _num_positive('timeout', timeout)
    _int_positive('ttl', ttl)
    # start
    with socket.socket(socket.AF_INET,
                       socket.SOCK_RAW,
                       socket.IPPROTO_ICMP) as conn:
        conn.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
        try:
            conn.connect((address, 0))
        except OSError as e:
            print(f'An error occurred while connecting to: [{address}]\n{e}')
            return None
        except Exception:
            raise
        else:
            id_ = threading.get_ident()
            result = Result(address)
            for seq in range(1, repeat + 1):
                packet = Icmp.pack(id_=id_, seq=seq, size=size)
                response = _ping_once(conn, address, packet, timeout)
                result.append(response)
                if seq < repeat:
                    time.sleep(interval)
            return result


def _ping_once(conn, address, packet, timeout):
    try:
        send_time = time.time()
        conn.send(packet)
        while True:
            readable, __, __ = select.select([conn], [], [], timeout)
            recv_packet = readable[0].recv(1024)
            rtt = time.time() - send_time
            return Response.valid(packet=recv_packet, rtt=rtt)
    except IndexError:
        return Response.timeout()
    except Exception:
        raise
