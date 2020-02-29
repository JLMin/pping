# -*- coding: utf-8 -*-

import statistics


class Result:

    def __init__(self, address):
        self.responses = list()
        self.times = list()
        self.rtts = list()
        self.status = 'ERROR'
        self.error = None

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
        if response.status == 'OK':
            self.status = 'OK'
            rtt = response.rtt
            self.times.append(rtt)
            self.rtts.append(rtt)
        else:
            self.error = response.error
            self.rtts.append(None)
        self.responses.append(response)

    def to_dict(self):
        d = dict()
        d['send'] = self.send
        return d
