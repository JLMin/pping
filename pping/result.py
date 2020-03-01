# -*- coding: utf-8 -*-

import statistics
import socket
from collections import namedtuple

from .packet import Icmp, IPv4


class Result:

    def __init__(self, address):
        (self.hostname,
         self.hostalias,
         self.iplist) = socket.gethostbyname_ex(address)
        self.responses = list()
        self.times = list()
        self.all_times = list()

    def __getitem__(self, key):
        return self.responses[key]

    def __str__(self):
        return '\n'.join(Result._prettify(r) for r in self.responses) + (
            f'\n\nPing statistics for {self.hostname}:\n'
            f'\tPackets: Sent = {self.sent}, '
            f'Received = {self.recv}, '
            f'Lost = {self.lost} ({round(self.lost / self.sent * 100)}% loss)\n'
            f'Approximate round trip times in milli-seconds:\n'
            f'\tAverage = {round(self.avg * 1000)}ms, '
            f'Minimum = {round(self.min * 1000)}ms, '
            f'Maximum = {round(self.max * 1000)}ms, '
            f'Stdev = {round(self.stdev * 1000,1)}'
        )

    def __repr__(self):
        return self.__str__()

    @staticmethod
    def _prettify(resp):
        if resp.status == Response.OK:
            return (
                f'Reply from {resp.src}: bytes={resp.size} '
                f'time={round(resp.rtt * 1000)}ms TTL={resp.ttl}'
            )
        else:
            return 'Request timed out.'

    @property
    def max(self):
        try:
            return max(self.times)
        except ValueError:
            return 0

    @property
    def min(self):
        try:
            return min(self.times)
        except ValueError:
            return 0

    @property
    def avg(self):
        try:
            return statistics.mean(self.times)
        except statistics.StatisticsError:
            return 0

    @property
    def stdev(self):
        try:
            return statistics.pstdev(self.times)
        except statistics.StatisticsError:
            return 0

    @property
    def sent(self):
        return len(self.responses)

    @property
    def recv(self):
        return len(self.times)

    @property
    def lost(self):
        return len(self.responses) - len(self.times)

    def append(self, response):
        if response.status == Response.OK:
            self.times.append(response.rtt)
            self.all_times.append(response.rtt)
        else:
            self.all_times.append(None)
        self.responses.append(response)


class Response:
    OK, TIMEDOUT = 'ok', 'timedout'

    _Valid = namedtuple('Response', ['status', 'src', 'dst', 'ttl',
                                     'size', 'seq', 'rtt'])

    @staticmethod
    def valid(*, packet, rtt):
        ipv4 = IPv4.unpack(packet[:20])
        icmp = Icmp.unpack(packet[20:])
        return Response._Valid(Response.OK, ipv4.src, ipv4.dst, ipv4.ttl,
                               len(icmp.payload), icmp.seq, rtt)

    _Error = namedtuple('Response', ['status'])

    @staticmethod
    def timeout():
        return Response._Error(Response.TIMEDOUT)
