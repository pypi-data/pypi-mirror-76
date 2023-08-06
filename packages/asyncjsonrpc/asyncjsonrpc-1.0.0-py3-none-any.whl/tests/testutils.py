import asyncio
import asyncjsonrpc

def req(method, *args, **kwargs):
    '''Construct a JSON-RPC request for the provided method and arugments'''

    return asyncjsonrpc.Request(
        method = method,
        params = args or kwargs,
        id = 1)

def asynctest(decorated):
    def inner(*args):
        asyncio.run(decorated(*args))

    return inner