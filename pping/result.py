# -*- coding: utf-8 -*-

import statistics
import socket
from collections import namedtuple

from .packet import Icmp, IPv4


class Result:

    def __init__(self, address):
        self.hostname, self.aliaslist, self.ipaddrlist = socket.gethostbyname_ex(address)
        self.responses = list()
        self._valid_times = list()
        self._all_times = list()

    def __getitem__(self, key):
        return self.responses[key]

    def __str__(self):
        return '\n'.join(Result.prettify(r) for r in self.responses) + (
            f'\n\nPing statistics:\n'
            f'Sent = {self.send}, Received = {self.recv}, Lost = {self.lost}\n'
            f'Avg = {round(self.avg * 1000)}ms, '
            f'Min = {round(self.min * 1000)}ms, '
            f'Max = {round(self.max * 1000)}ms, '
            f'Std = {round(self.stdev * 1000,1)}'
        )

    @staticmethod
    def prettify(resp):
        return (
            f'Reply from {resp.src}: bytes={resp.size} '
            f'time={round(resp.rtt * 1000)}ms TTL={resp.ttl}'
        )

    @property
    def max(self):
        try:
            return max(self._valid_times)
        except ValueError:
            return 0

    @property
    def min(self):
        try:
            return min(self._valid_times)
        except ValueError:
            return 0

    @property
    def avg(self):
        try:
            return statistics.mean(self._valid_times)
        except statistics.StatisticsError:
            return 0

    @property
    def stdev(self):
        try:
            return statistics.pstdev(self._valid_times)
        except statistics.StatisticsError:
            return 0

    @property
    def send(self):
        return len(self.responses)

    @property
    def recv(self):
        return len(self._valid_times)

    @property
    def lost(self):
        return len(self.responses) - len(self._valid_times)

    def append(self, response):
        if response.status == Response.OK:
            self._valid_times.append(response.rtt)
            self._all_times.append(response.rtt)
        else:
            self._all_times.append(None)
        self.responses.append(response)

    def to_dict(self):
        d = dict()
        d['send'] = self.send
        return d


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
