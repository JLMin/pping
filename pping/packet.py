import socket
import struct
from collections import namedtuple

from .utils import checksum


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

    ICMP_Data = namedtuple('ICMP_Data',
                           ['type', 'code', 'checksum', 'id', 'seq', 'payload'])

    @staticmethod
    def pack(*, id_, seq, size):
        # Since we only send ICMP ping request, so the type and code are fixed,
        # Type for echo requeat is '8', code for echo is always '0'
        _type, _code = 8, 0
        v_id   = int(id_) & 0xffff
        v_seq  = int(seq) & 0xffff
        v_data = ('x' * size).encode('utf8')
        pack_format = f'!BBHHH{size}s'

        # temp packet, for calculate the real checksum
        temp_cksum  = 0
        temp_packet = struct.pack(pack_format, _type, _code,
                                  temp_cksum, v_id, v_seq, v_data)
        # real packet, this one for send ping request
        icmp_cksum  = checksum(temp_packet)
        icmp_packet = struct.pack(pack_format, _type, _code,
                                  icmp_cksum, v_id, v_seq, v_data)
        return icmp_packet

    @staticmethod
    def unpack(icmp_packet):
        icmp_header   = icmp_packet[:8]
        icmp_payload  = icmp_packet[8:]
        unpack_format = '!BBHHH'
        unpacked_data = struct.unpack(unpack_format, icmp_header)
        return Icmp.ICMP_Data(*unpacked_data, icmp_payload)


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

    IPv4_Data = namedtuple('IPv4_Data',
                           ['ver', 'dscp', 'length', 'id', 'flag', 'ttl',
                            'protocaol', 'checksum', 'src', 'dst'])

    @staticmethod
    def pack(*, src, dst, ttl):
        # This method is only used to construct a fake package for testing.

        # hard-coded, fake value
        f_vi = ((4 << 4) + 5) & 0xff
        f_ds = 0x0
        f_len = 60
        f_id = 1
        f_flags = 0
        f_proto = 1  # ICMP
        f_cksum = 0
        # args
        v_ttl = int(ttl) & 0xff
        v_src = socket.inet_aton(src)
        v_dst = socket.inet_aton(dst)
        pack_format = f'!BBHHHBBH{len(v_src)}s{len(v_dst)}s'
        ipv4_header = struct.pack(pack_format, f_vi, f_ds, f_len,
                                  f_id, f_flags, v_ttl, f_proto,
                                  f_cksum, v_src, v_dst)
        return ipv4_header

    @staticmethod
    def unpack(ipv4_header):
        unpack_format = '!BBHHHBBH'
        unpacked_data = struct.unpack(unpack_format, ipv4_header[:12])
        ip_src = socket.inet_ntoa(ipv4_header[12:16])
        ip_dst = socket.inet_ntoa(ipv4_header[16:20])
        return IPv4.IPv4_Data(*unpacked_data, ip_src, ip_dst)
