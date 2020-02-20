"""
This module provides two functions for
creating ICMP packet to send ping request and for
reading data from the responding ICMP packet.

Functions:
    pack(id_: int, seq: int, data: str)
        -- create a ICMP packet for ping.
    unpack(packet: bytes)
        -- read data from a ICMP packet from response.

Object:
    _PacketData
        -- namedtuple, store the data from unpack function.
"""


import struct
from collections import namedtuple


def pack(id_: int, seq: int, data: str):
    packet = _icmp_packet(id_, seq, data)
    return packet


def _icmp_packet(id_, seq, data):
    """
    ICMP Header (8 bytes) & ICMP Payload
    +--------+--------+----------------+
    |  type  |  code  |    checksum    |
    +--------+--------+----------------+
    |   identifier    |    sequence    |
    +-----------------+----------------+
    |              payload             |
    +----------------------------------+
    """

    ECHO_REQUEST = 8
    ECHO_CODE    = 0
    v_id   = _to_16bits_int(id_)
    v_seq  = _to_16bits_int(seq)
    v_data = _to_bytes(data)
    pack_format = f'!BBHHH{len(v_data)}s'

    # temp packet, for calculate the real checksum
    temp_cksum  = 0
    temp_packet = struct.pack(pack_format, ECHO_REQUEST, ECHO_CODE,
                              temp_cksum, v_id, v_seq, v_data)
    # real packet, this one for send ping request
    icmp_cksum  = _checksum(temp_packet)
    icmp_packet = struct.pack(pack_format, ECHO_REQUEST, ECHO_CODE,
                              icmp_cksum, v_id, v_seq, v_data)
    return icmp_packet


def _to_16bits_int(int_num):
    try:
        value = int(int_num) & 0xffff
    except (TypeError, ValueError):
        value = 1
    return value


def _to_bytes(data):
    string = str(data)
    bytes_ = string.encode('utf8')
    return bytes_


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


_PacketData = namedtuple('PacketData',
                         ['ip_src', 'ip_dst', 'ip_ttl',
                          'type', 'code', 'cksum', 'id', 'seq', 'payload'])


def unpack(packet: bytes):
    ipv4_data = _ipv4_unpack(packet)
    icmp_data = _icmp_unpack(packet)
    packet_data = _PacketData(*ipv4_data, *icmp_data)
    return packet_data


def _ipv4_unpack(packet):
    ip_header = packet[:20]
    ip_src = '.'.join(str(x) for x in ip_header[12:16])
    ip_dst = '.'.join(str(x) for x in ip_header[16:20])
    ip_ttl = ip_header[8]
    return ip_src, ip_dst, ip_ttl


def _icmp_unpack(packet):
    icmp_header = packet[20:28]
    icmp_payload = packet[28:]
    unpack_format = '!BBHHH'
    datas = struct.unpack(unpack_format, icmp_header)
    return *datas, icmp_payload


def verify(packet, v_id, v_seq):
    pass
