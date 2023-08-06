# libsocks

a socks5/socks proxy client module, easy to work with your code

# Feature

* socks4 `CONNECT` command support

* socks5 `CONNECT` command support

* Username/Password Authentication support for SOCKS V5

* TCP supported

* work with sync/asyncio

# Requirements

* Python3.5+ support

# Usage

## blocking socket example

```python
import urllib2
import socket
import socks

socks.set_default_proxy(socks.SOCKS5, "localhost")
socket.socket = socks.socksocket
```
