import asyncio
import random

from typing import Union, Dict, Any

from ..exceptions import RpcError, UnexpectedResponseError
from ..request import Request
from ..response import Response

class BaseClient:
    """Connects to JSON-RPC servers, sends Requests, and dispatches Responses.
    
    This base class is not a functional client, a subclass must be used instead.
    """

    def __init__(self):
        """Initializes a BaseClient instance."""

        self.__call_events__: Dict[int, asyncio.Event] = {}
        self.__call_responses__: Dict[int, Response] = {}

    def __getattr__(self, method_name):
        """Generates and returns a wrapper method around call when an undefined attribute of BaseClass is accessed.
        """

        def _call(*args, **kwargs):
            return self.call(method_name, *args, **kwargs)

        return _call

    async def call(self, method_name: str, *args: Any, **kwargs: Any) -> Any:
        """Creates and sends a Request with the method name and arguments provided, then awaits a Response.

        Args:
            method_name: Name of the remote method to call
            *args: Positional arguments for the method call
            **kwargs: Keyword arguments for the method call

        Raises:
            ValueError: Raised if method is called with both positional and keyword arguments.
            asyncio.RpcError: Raised if the method call results in an exception.

        Returns:
            Result of the method call.
        """        
        if args and kwargs:
            raise ValueError('cannot make JSON-RPC call with both positional and keyword arguments')

        id = random.randint(1, 10**6)
        while id in self.__call_events__:
            id = random.randint(1, 10**6)

        event = self.__call_events__[id] = asyncio.Event()

        request = Request(
            method_name,
            params = args or kwargs or None,
            id = id)

        await self._send_request(request)
        await event.wait()

        response = self.__call_responses__[id]

        del self.__call_events__[id]
        del self.__call_responses__[id]

        if response.error:
            raise response.exception

        return response.result

    async def _send_request(self, request: Request) -> None:
        """Sends a Request to a JSON-RPC server.

        Not implemented by BaseClient, must be overridded by a subclass.

        Raises:
            NotImplementedError: If base class's implementation is called.
        """

        raise NotImplementedError('must be overridden by subclass')

    def _response_received(self, response: Response) -> None:
        """Dispatches a Response received from a JSON-RPC server.

        Never called by BaseClient, must be called by a subclass.
        """

        if response.notification_error:
            self._notification_error_received(response)

        id = response.id
        if not id in self.__call_events__:
            raise UnexpectedResponseError(f'did not expect response with id {response.id}')

        self.__call_responses__[id] = response
        self.__call_events__[id].set()

    def _notification_error_received(self, notification: Response) -> None:
        """Handles a Response describing a notification error received from a JSON-RPC server.

        Base class' implementation does nothing, must be implemented by subclass if needed.
        """

        return