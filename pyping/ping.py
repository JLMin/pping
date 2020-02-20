import socket
import select
import time
from collections import namedtuple

import pyping._packet as packet


def ping(address, id_=1, seq=1, data='data'):
    """
    send a ping request to a ip address
    returns a namedtuple (_PingResult) which stores the ping result
    """

    icmp_packet = packet.pack(id_, seq, data)
    with socket.socket(socket.AF_INET,
                       socket.SOCK_RAW,
                       socket.getprotobyname('icmp')) as conn:
        try:
            conn.connect((address, 0))
            send_time = _send(conn, icmp_packet)
            recv_time, recv_packet = _recv(conn)
        except IndexError:
            return _result('Request timed out.')
        except (socket.gaierror, OSError) as e:
            try:
                error_msg = socket.errorTab[e.errno]
            except KeyError:
                error_msg = f'Unknow error: {e}'
            return _result(error_msg)
        else:
            packet_data = packet.unpack(recv_packet)
            response_time = recv_time - send_time
            return _result(None, packet_data, response_time)


def _send(conn, packet):
    send_time = time.time()
    conn.send(packet)
    return send_time


def _recv(conn):
    while True:
        readable, __, __ = select.select([conn], [], [], 1)
        recv_packet = readable[0].recv(1024)
        recv_time = time.time()
        return recv_time, recv_packet


_PingResult = namedtuple('PingResult', ['error', 'data', 'time'])


def _result(error, data=None, time=None):
    return _PingResult(error, data, time)
