# -*- coding: utf-8 -*-

import statistics
import socket
from collections import namedtuple

from .packet import Icmp, IPv4


class Result:

    def __init__(self, address):
        self.hostname, self.aliaslist, self.ipaddrlist = socket.gethostbyname_ex(address)
        self.responses = list()
        self.times = list()
        self.rtts = list()

    def __getitem__(self, key):
        return self.responses[key]

    def __str__(self):
        return (
            f'send={self.send}, recv={self.recv}, lost={self.lost}, '
            f'avg={round(self.avg * 1000)}ms, '
            f'min={round(self.min * 1000)}ms, '
            f'max={round(self.max * 1000)}ms, '
            f'std={round(self.stdev * 1000,1)}'
        )

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
    def send(self):
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
            self.rtts.append(response.rtt)
        else:
            self.rtts.append(None)
        self.responses.append(response)

    def to_dict(self):
        d = dict()
        d['send'] = self.send
        return d


class Response:

    OK = 'ok'
    TIMEDOUT = 'timedout'

    _Valid = namedtuple('Response', ['status', 'src', 'dst',
                                     'ttl', 'seq', 'rtt'])

    _Error = namedtuple('Response', ['status'])

    @staticmethod
    def valid(*, packet, rtt):
        ipv4_data = IPv4.unpack(packet[:20])
        icmp_data = Icmp.unpack(packet[20:])
        return Response._Valid(Response.OK, ipv4_data.src, ipv4_data.dst,
                               ipv4_data.ttl, icmp_data.seq, rtt)

    @staticmethod
    def timeout():
        return Response._Error(Response.TIMEDOUT)
