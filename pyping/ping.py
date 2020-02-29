# -*- coding: utf-8 -*-

import select
import socket
import threading
import time
from collections import namedtuple

from .packet import Icmp
from .result import Result


def ping(address, **kwargs):
    def prepare_args(data='data', repeat=4, interval=1):
        return data, repeat, interval

    data, repeat, interval = prepare_args(**kwargs)
    return _ping(address, data, repeat, interval)


def _ping(*, address, data, repeat, interval):
    id_ = threading.get_ident()
    result = Result(address)
    for seq in range(1, repeat + 1):
        packet = Icmp.pack(id_=id_, seq=seq, data=data)
        response = _ping_once(address=address, packet=packet)
        result.append(response)
        if seq < repeat:
            time.sleep(interval)
    return result


def _ping_once(*, address, packet):
    with socket.socket(socket.AF_INET,
                       socket.SOCK_RAW,
                       socket.IPPROTO_ICMP) as conn:
        try:
            conn.connect((address, 0))
            send_time = time.time()
            conn.send(packet)
            while True:
                readable, __, __ = select.select([conn], [], [], 1)
                recv_packet = readable[0].recv(1024)
                rtt = time.time() - send_time
                return Response.valid(packet=recv_packet, rtt=rtt)
        except IndexError:
            return Response.error(err_msg='Request timed out.')
        except OSError as e_os:
            try:
                error_msg = socket.errorTab[e_os.errno]
            except (AttributeError, KeyError):
                error_msg = e_os
            except Exception as e_unknow:
                error_msg = e_unknow
            return Response.error(err_msg=error_msg)
        except Exception as e_unknow:
            return Response.error(err_msg=e_unknow)


class Response:
    _Valid = namedtuple('Response', ['status',
                                     'src', 'dst', 'ttl',
                                     'id_', 'seq', 'data',
                                     'rtt'])

    _Error = namedtuple('Response', ['status', 'error'])

    @staticmethod
    def valid(*, packet, rtt):
        ipv4_data = IPv4.unpack(packet[:20])
        icmp_data = Icmp.unpack(packet[20:])
        return Response._Valid('OK', *ipv4_data, *icmp_data, rtt)

    @staticmethod
    def error(*, err_msg):
        return Response._Error('ERROR', err_msg)
