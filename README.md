# pping

## **ping** in python

usage:

```python
from pping import ping

# simple usage
result = ping('www.example.com')

# full arguments (default value)
result = ping('www.example.com',
              repeat=4,    # Number of echo requests to send.
              interval=1,  # Time in seconds interval between each request.
              size=32,     # Send buffer size in bytes.
              timeout=1,   # Timeout in seconds to wait for each reply.
              ttl=128)     # Time To Live.

# result properties
print(result)
result[index]
# host
result.hostname
result.aliaslist
result.ipaddrlist
# route trip time
result.times      # timed out are not inclued
result.all_times  # timed out as None
result.avg
result.min
result.max
result.stdev
# packets
result.sent
result.recv
result.lost
```
