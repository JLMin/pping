[![PyPI](https://img.shields.io/badge/pypi-0.0.6-blue)](https://pypi.org/project/pping/)
[![Coverage](https://img.shields.io/badge/coverage-95%25-green)](https://github.com/JLMin/pping)
[![GitHub license](https://img.shields.io/github/license/JLMin/pping)](https://github.com/JLMin/pping/blob/master/LICENSE)

# pping

**ping** in python

## Installing

```python
pip install pping
```

## Usage

```python
from pping import ping
result = ping('www.example.com') # simple usage
result = ping('www.example.com', # optional arguments
              repeat=4,          # -- Number of echo requests to send.
              interval=1,        # -- Time in seconds interval between each request.
              size=32,           # -- Send buffer size in bytes.
              timeout=1,         # -- Timeout in seconds to wait for each reply.
              ttl=128)           # -- Time To Live.
```

## Operation on the result

```python
>>> print(result)
'''
Reply from 93.184.216.34: bytes=32 time=151ms TTL=52
Request timed out.
Reply from 93.184.216.34: bytes=32 time=149ms TTL=52
Reply from 93.184.216.34: bytes=32 time=150ms TTL=52

Ping statistics for www.example.com:
        Packets: Sent = 4, Received = 3, Lost = 1 (25% loss)
Approximate round trip times in milli-seconds:
        Average = 150ms, Minimum = 149ms, Maximum = 151ms, Stdev = 0.5
'''
```

```python
>>> result[0]
Response(status='ok', src='93.184.216.34', dst='192.168.31.100', ttl=52, size=32, seq=1, rtt=0.15059328079223633)

>>> result[1]
Response(status='timedout')
```

```python
>>> result.hostname
'www.example.com'

>>> result.iplist
['93.184.216.34']
```

```python
>>> result.times      # timed out are not inclued
[0.15059328079223633, 0.1492629051208496, 0.14995193481445312]

>>> result.all_times  # timed out as None
[0.15059328079223633, None, 0.1492629051208496, 0.14995193481445312]
```

```python
# other properties
>>> result.hostalias
>>> result.avg
>>> result.min
>>> result.max
>>> result.stdev
>>> result.sent
>>> result.recv
>>> result.lost
```

## License

This project is licensed under the MIT License - see the LICENSE file for details
