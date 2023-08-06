import asyncio
import aiohttp
from aiohttp import web

from .base_server import BaseServer
from ..request import Request

class AiohttpWebsocketServer(BaseServer):
    """An asyncjsonrpc server subclass designed to handle JSON-RPC over WebSockets via aiohttp.

        Typical usage example:
        
        >>> methods = asyncjsonrpc.MethodGroup()
        >>> rpcserver = asyncjsonrpc.server.AiohttpWebsocketServer(methods)
        >>> app.add_routes([web.get('/', rpcserver)])
        >>> web.run_app(app)
    """

    async def __call__(self, request: web.Request) -> None:
        """Listens for Requests from a client and creates tasks to handle them.

        This method overrides __call__() to be compatible with aiohttp.

        Args:
            request: aiohttp request.
        """

        loop = asyncio.get_event_loop()

        ws = web.WebSocketResponse()
        await ws.prepare(request)

        async for msg in ws:
            if msg.type == aiohttp.WSMsgType.TEXT:
                loop.create_task(self._handle_data(msg.data, ws))

    async def _handle_data(self, data: str, ws: web.WebSocketResponse) -> None:
        """Handles a JSON-RPC Request and sends a Response.

        Args:
            data: JSON-encoded request data.
            ws: WebSocket to which the Response will be sent.
        """        

        request = Request.from_json(data)
        response = await self._dispatch_request(request)
        response_json = response.json()

        if response_json:
            await ws.send_str(response_json)