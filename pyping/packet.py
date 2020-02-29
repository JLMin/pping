# -*- coding: utf-8 -*-

"""
This module handles ICMP and IPv4 headers.
"""

import struct
import socket
from collections import namedtuple


class Icmp:
    """
    The ICMP header structure:

    ICMP Header (8 bytes) & ICMP Payload
    +--------+--------+----------------+
    |  type  |  code  |    checksum    |
    +--------+--------+----------------+
    |   identifier    |    sequence    |
    +-----------------+----------------+
    |              payload             |
    +----------------------------------+
    """

    ICMP_Data = namedtuple('ICMP_Data', ['id_', 'seq', 'data'])

    @staticmethod
    def pack(*, id_=1, seq=1, data=''):
        # Since we only send ICMP ping request, so the type and code are fixed,
        # Type for echo requeat is '8', code for echo is always '0'
        _type, _code = 8, 0
        v_id   = int(id_) & 0xffff
        v_seq  = int(seq) & 0xffff
        v_data = data.encode('utf8')
        pack_format = f'!BBHHH{len(v_data)}s'

        # temp packet, for calculate the real checksum
        temp_cksum  = 0
        temp_packet = struct.pack(pack_format, _type, _code,
                                  temp_cksum, v_id, v_seq, v_data)
        # real packet, this one for send ping request
        icmp_cksum  = _checksum(temp_packet)
        icmp_packet = struct.pack(pack_format, _type, _code,
                                  icmp_cksum, v_id, v_seq, v_data)
        return icmp_packet

    @staticmethod
    def unpack(icmp_packet):
        # only the data of interest is kept and the rest is discarded
        try:
            icmp_header   = icmp_packet[:8]
            icmp_payload  = icmp_packet[8:].decode('utf8')
            unpack_format = '!BBHHH'
            _, _, _, id_, seq = struct.unpack(unpack_format, icmp_header)
            return Icmp.ICMP_Data(id_, seq, icmp_payload)
        except TypeError:
            return Icmp.ICMP_Data(None, None, None)


class IPv4:
    """
    The IPv4 header structure:

    IPv4 Header (20 bytes)
    +--------+--------+----------------+
    | V. IHL |  DSCP  |     length     |
    +--------+--------+----------------+
    |   identifier    | flags & offset |
    +--------+--------+----------------+
    |  TTL.  |protocol|    checksum    |
    +--------+--------+----------------+
    |        Source IP address         |
    +--------+--------+----------------+
    |      Destination IP address      |
    +--------+--------+----------------+
    """

    IPv4_Data = namedtuple('IPv4_Data', ['src', 'dst', 'ttl'])

    @staticmethod
    def pack(*, src, dst, ttl):
        # Socket will automatically create ipv4 header.
        # This method is used to construct a fake package for testing.
        # Because of that, only 3 of the fields are needed,
        # which are 'source', 'destination' and 'time to live'

        # hard-coded, fake data
        f_vi = ((4 << 4) + 5) & 0xff
        f_ds = 0x0
        f_len = 60
        f_id = 1
        f_flags = 0
        f_proto = 1  # ICMP
        f_cksum  = 0
        # valid data
        v_ttl = int(ttl) & 0xff
        v_src = socket.inet_pton(socket.AF_INET, src)
        v_dst = socket.inet_pton(socket.AF_INET, dst)
        pack_format = f'!BBHHHBBH{len(v_src)}s{len(v_dst)}s'
        ipv4_packet = struct.pack(pack_format, f_vi, f_ds, f_len,
                                  f_id, f_flags, v_ttl, f_proto, f_cksum,
                                  v_src, v_dst)
        return ipv4_packet

    @staticmethod
    def unpack(ip_packet):
        # only the data of interest is kept and the rest is discarded
        try:
            src = socket.inet_ntoa(ip_packet[12:16])
            dst = socket.inet_ntoa(ip_packet[16:20])
            ttl = ip_packet[8]
            return IPv4.IPv4_Data(src, dst, ttl)
        except TypeError:
            return IPv4.IPv4_Data(None, None, None)


def _checksum(packet):
    cksum = 0
    for i in range(0, len(packet), 2):
        try:
            cksum += packet[i] + (packet[i + 1] << 8)
        except IndexError:  # packet size is odd
            cksum += packet[i]
        cksum = (cksum & 0xffff) + (cksum >> 16)
    cksum = ~cksum & 0xffff
    cksum = cksum >> 8 | (cksum << 8 & 0xff00)
    return cksum
