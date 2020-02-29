# piping

## Implemented '**ping**' command by using python

usage:

```python
from pyping import ping

# simple usage
result = ping('www.example.com')

# full arguments (default value)
result = ping('www.example.com',
              repeat=4,    # Number of echo requests to send.
              interval=1,  # Time in seconds interval between each request.
              size=32,     # Send buffer size in bytes.
              timeout=1,   # Timeout in seconds to wait for each reply.
              ttl=128)     # Time To Live.
```
