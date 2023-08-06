# asyncjsonrpc

An asynchronous JSON-RPC client/server for Python. Currently supports WebSocket transports, though more may be added in the future.

[Module documentation](https://hunteradasmith.gitlab.io/asyncjsonrpc/index.html)
[asyncjsonrpc on PyPi](https://pypi.org/project/asyncjsonrpc/)

# Install

Install from PyPi via pip:

    pip3 install asyncjsonrpc

# Features

* Compliant with the JSON-RPC 2.0 specification
* Transport-agnostic design, could potentially work with any network protocol supported by Python and asyncio
* JSON-RPC over WebSockets support via [aiohttp](https://docs.aiohttp.org/en/stable/)

### Unimplemented JSON-RPC Features

* Batched requests
* Manifests


# Examples

See the examples directory for more.

### Quick server example

```python
import asyncjsonrpc
from aiohttp import web

methods = asyncjsonrpc.MethodGroup()

@methods.method
def greet(name):
    return f'Hello {name}!'

rpcserver = asyncjsonrpc.server.AiohttpWebsocketServer(methods)
app = web.Application()
app.add_routes([web.get('/', rpcserver)])
web.run_app(app)
```

### Quick client example

```python
import asyncjsonrpc, asyncio
from aiohttp import web

async def main():
    client = asyncjsonrpc.client.AiohttpWebsocketClient()
    await client.connect('http://localhost:8080/')
    print(await client.greet('world'))

asyncio.run(main())
```