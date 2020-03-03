import statistics
import socket

from .session import Response


class Result:

    __slots__ = ['responses', 'times', 'all_times',
                 'hostname', 'hostalias', 'iplist',
                 'sent', 'recv', 'lost',
                 'max', 'min', 'avg', 'stdev']

    def __init__(self, addr, resps):
        (self.hostname,
         self.hostalias,
         self.iplist) = socket.gethostbyname_ex(addr)

        self.responses = resps
        self.times     = [r.rtt for r in resps if 'rtt' in r._fields]
        self.all_times = [r.rtt if 'rtt' in r._fields else None for r in resps]

        self.sent = len(self.responses)
        self.recv = len(self.times)
        self.lost = self.sent - self.recv

        self.max   = max(self.times) if self.times else 0
        self.min   = min(self.times) if self.times else 0
        self.avg   = statistics.mean(self.times) if self.times else 0
        self.stdev = statistics.pstdev(self.times) if self.times else 0

    def __str__(self):
        if self.recv > 0:
            return '\n'.join(Result._prettify(r) for r in self.responses) + (
                f'\n\nPing statistics for {self.hostname}:\n'
                f'\tPackets: Sent = {self.sent}, '
                f'Received = {self.recv}, '
                f'Lost = {self.lost} '
                f'({round(self.lost / self.sent * 100)}% loss)\n'
                f'Approximate round trip times in milli-seconds:\n'
                f'\tAverage = {round(self.avg * 1000)}ms, '
                f'Minimum = {round(self.min * 1000)}ms, '
                f'Maximum = {round(self.max * 1000)}ms, '
                f'Stdev = {round(self.stdev * 1000,1)}'
            )
        else:
            return self.responses[0].error

    def __repr__(self):
        return (
            f'{self.__class__.__name__} of [{self.hostname}] > '
            f'{round(self.avg * 1000)}ms ~ {round(self.stdev * 1000,1)} '
            f'[{self.recv}/{self.sent}, L:{self.lost}]'
        )

    def __getitem__(self, key):
        return self.responses[key]

    @staticmethod
    def _prettify(resp):
        if resp.status == Response.OK:
            return (
                f'Reply from {resp.src}: bytes={resp.size} '
                f'time={round(resp.rtt * 1000)}ms TTL={resp.ttl}'
            )
        else:
            return resp.error
