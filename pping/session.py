import select
import socket
from collections import namedtuple
from time import sleep, time

from .packet import Icmp, IPv4


class Request:

    @staticmethod
    def ping(*, address, repeat, interval, size, timeout, ttl):
        with socket.socket(socket.AF_INET,
                           socket.SOCK_RAW,
                           socket.IPPROTO_ICMP) as conn:
            conn.setsockopt(socket.SOL_IP, socket.IP_TTL, ttl)
            try:
                conn.connect((address, 0))
            except OSError as e:
                return [Response._error(str(e))]
            else:
                return list(Request._ping_multiple(conn, repeat, interval,
                                                   size, timeout))

    @staticmethod
    def _ping_multiple(conn, repeat, interval, size, timeout):
        for seq in range(1, repeat + 1):
            packet = Icmp.pack(id_=id(conn), seq=seq, size=size)
            yield Request._ping_single(conn, packet, timeout)
            if seq < repeat:
                sleep(interval)

    @staticmethod
    def _ping_single(conn, packet, timeout):
        send_time = time()
        conn.send(packet)
        while True:
            readable, _, _ = select.select([conn], [], [], timeout)
            try:
                reply = readable[0].recv(1024)
            except IndexError:
                return Response._timeout()
            else:
                return Response._valid(packet=reply,
                                       rtt=time() - send_time)


class Response:

    OK, TIMEDOUT, ERROR = 'ok', 'timedout', 'error'

    _Valid = namedtuple('Response', ['status', 'src', 'dst', 'ttl',
                                     'size', 'seq', 'rtt'])

    _Error = namedtuple('Response', ['status', 'error'])

    @staticmethod
    def _valid(*, packet, rtt):
        ipv4 = IPv4.unpack(packet[:20])
        icmp = Icmp.unpack(packet[20:])
        return Response._Valid(Response.OK, ipv4.src, ipv4.dst, ipv4.ttl,
                               len(icmp.payload), icmp.seq, rtt)

    @staticmethod
    def _timeout():
        return Response._Error(Response.TIMEDOUT, 'Request timed out.')

    @staticmethod
    def _error(err_msg):
        return Response._Error(Response.ERROR, err_msg)
