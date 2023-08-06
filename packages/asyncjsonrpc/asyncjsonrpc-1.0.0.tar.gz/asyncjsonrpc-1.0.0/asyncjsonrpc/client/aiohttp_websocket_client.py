import asyncio
import aiohttp
from typing import Callable

from .base_client import BaseClient
from ..request import Request
from ..response import Response
from ..method_group import MethodGroup

class AiohttpWebsocketClient(BaseClient):
    """An asyncjsonrpc client subclass designed to handle JSON-RPC over WebSockets via aiohttp.

        Typical usage example:

        >>> client = asyncjsonrpc.client.AiohttpWebsocketClient()
        >>> await client.connect('http://localhost:8080/')
        >>> await client.call('method')

    Attributes:
        connected: States whether this client is currently connected to a server.
        on_connected: A callback that is called when this client establishes a connection. The
            callback is not passed any parameters.
        on_disconnected: A callback that is called when this client ends or loses
            a connection, called on both intentionall disconnections and on errors. The callback is passed two
            parameters: a bool that is True if the disconnection was intentional (i.e. the result of disconnect())
            and False if caused by an error, and an Exception if one is avaiable (otherwise None).
    """

    def __init__(
        self,
        on_connected: Callable[[], None] = None,
        on_disconnected: Callable[[bool, Exception], None] = None) -> None:
        """Initializes this AiohttpWebsocketClient.

        Keyword Arguments:
            on_connected: A callback that is called when this client establishes a connection. The
                callback is not passed any parameters. (default: None)
            on_disconnected: A callback that is called when this client ends or loses a connection,
                called on both intentionall disconnections and on errors. The callback is passed two
                parameters: a bool that is True if the disconnection was intentional (i.e. the result of
                disconnect()) and False if caused by an error, and an Exception if one is avaiable
                (otherwise None). (default: None)
        """

        super().__init__()

        self.__connected_event__ = asyncio.Event()
        self.__disconnected_event__ = asyncio.Event()
        self.__connect__task__: asyncio.Task = None

        self.__connecting_finished__: asyncio.Task = asyncio.Event()
        self.__connection_failed_reason__: Exception = None

        self.__session__ = aiohttp.ClientSession()
        self.__ws__: aiohttp.ClientWebSocketResponse = None

        self.__request_json_queue__ = asyncio.Queue()
        self.__request_queue_handler_task__: asyncio.Task = None

        self.connected = False
        self.on_connected: Callable[[], None] = on_connected
        self.on_disconnected = on_disconnected

    async def connect(self, url: str) -> None:
        """Establishes a connection to a JSON-RPC server.

        This coroutine waits until the connection is established before returning. If already connected, returns
        immediately.

        Arguments:
            url: The URL to which this client should connect.
        """

        if self.connected: return

        loop = asyncio.get_event_loop()
        self.__connect__task__ = loop.create_task(self._connect(url))
        self.__request_queue_handler_task__ = asyncio.create_task(self._request_queue_handler())

        await self.__connecting_finished__.wait()

        if self.__connection_failed_reason__:
            raise self.__connection_failed_reason__

    async def disconnect(self) -> None:
        """Ends a connection to a JSON-RPC server.

        This coroutine waits until the connection has been ended before returned. If not connected, returns immediately.
        """

        if not self.connected: return

        self.__request_queue_handler_task__.cancel()
        self.__connect__task__.cancel()

        await self.__disconnected_event__.wait()
 
    async def _connect(self, url: str) -> None:
        """Internally handles the client's WebSocket connection.

        Loops infinitely, opening a connection to the specified URL and waiting for incomming messages.

        If the connection drops due to a network error, calls the _on_disconnected method with any available
        exception.
        """

        self.__connecting_finished__.clear()
        self.__connection_failed_reason__ = None

        while True:
            try:
                async with self.__session__ as session:
                    async with session.ws_connect(url) as ws:
                        self.__ws__ = ws
                        self._on_connected()

                        async for msg in ws:
                            if msg.type == aiohttp.WSMsgType.TEXT:
                                self._parse_response(msg.data)
                            elif msg.type == aiohttp.WSMsgType.ERROR:
                                break

            except asyncio.CancelledError as e:
                self._on_disconnected(True, None)
                raise
            except Exception as e:
                self._on_disconnected(False, e)
                continue

            self._on_disconnected(False, None)

    def _on_connected(self) -> None:
        """Sets attributes and events and calls callbacks to indicate an established connection."""

        self.connected = True

        self.__connecting_finished__.set()

        self.__connected_event__.set()
        self.__disconnected_event__.clear()

        if self.on_connected:
            self.on_connected()

    def _on_disconnected(self, intentional: bool, exception: Exception) -> None:
        """Sets attributes and events and calls callbacks to indicate an ended connection."""

        self.connected = False

        if not self.__connecting_finished__.is_set():
            self.__connection_failed_reason__ = exception
            self.__connecting_finished__.set()

        self.__connected_event__.clear()
        self.__disconnected_event__.set()

        if self.on_disconnected:
            self.on_disconnected(intentional, exception)

    def _parse_response(self, data: str) -> None:
        """Parses a Response and sends it to the base class."""

        response = Response.from_json(data)
        self._response_received(response)

    async def _send_request(self, request: Request) -> None:
        """Queues a Request to be sent to the server."""

        request_json = request.json()
        if request_json:
            await self.__request_json_queue__.put(request_json)

    async def _request_queue_handler(self) -> None:
        """Sends queues Requests to the server."""

        while True:
            await self.__connected_event__.wait()

            request_json = await self.__request_json_queue__.get()
            await self.__ws__.send_str(request_json)