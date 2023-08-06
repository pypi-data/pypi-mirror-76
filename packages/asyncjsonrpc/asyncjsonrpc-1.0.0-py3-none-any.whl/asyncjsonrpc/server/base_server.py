from __future__ import annotations

import asyncio
import inspect
from typing import Union, Dict, Callable, Any

from ..exceptions import NoMethodError, InvalidParametersError
from ..request import Request
from ..response import Response
from ..method_group import MethodGroup

def params_match_signature(method: Callable, params: Union[list, dict]) -> bool:
    if params == None or len(params) == 0:
        return True

    signature = inspect.signature(method)
    sig_params = signature.parameters.values()
    sig_param_kinds = [p.kind for p in sig_params]

    is_var_positional = inspect.Parameter.VAR_POSITIONAL in sig_param_kinds
    positional_count = len([p for p in sig_param_kinds if p in (
        inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)])

    is_var_keyword = inspect.Parameter.VAR_KEYWORD in sig_param_kinds
    keywords = [p.name for p in sig_params if p.kind in (
        inspect.Parameter.KEYWORD_ONLY, inspect.Parameter.POSITIONAL_OR_KEYWORD)]

    if type(params) == dict:
        return is_var_keyword or all(k in keywords for k in params.keys())
    else:
        return is_var_positional or len(params) <= positional_count


def call_with_params(method: Callable, params: Union[list, dict]) -> Any:
    if params == None:
        return method()
    elif isinstance(params, dict):
        return method(**params)
    else:
        return method(*params)

class BaseServer:
    """Receives Requests, runs requested methods, and returns Responses.
    
    This base method is not a functional server, a subclass must be used instead.
    
    Attributes:
        on_request: An optional callback called when this server receives a request. The
            callback is passed the Request object as its only argument.
        on_response: An optional callback called when this server sends a
            response. The callback is passed the both the Reqeust and Response objects.
    """

    def __init__(
        self,
        method_group: MethodGroup,
        on_request: Callable[[Request], None] = None,
        on_response: Callable[[Request, Response], None] = None):
        """Initializes a BaseServer instance.
        
        Arguments:
            method_group: MethodGroup instance containing references to the methods for which this
                server will dispatch requests.
            on_request: An optional callback called when this server receives a request.
                The callback is passed the Request object as its only argument. (default: None)
            on_response: An optional callback called when this server sends a
                response. The callback is passed the both the Request and Response objects. (default: None)
        """

        self.on_request = on_request
        self.on_response = on_response

        self.__method_group__ = method_group

    async def _dispatch_request(self, request: Request) -> Response:
        """Runs a method specified by the provided request and returns a Response.

        Arguments:
            request: JSON-RPC Request to be dispatched.

        Returns:
            Response indicating either the result of the request, or the details of an error encountered
                while processing the request or running the requested method.
        """

        self._on_request(request)

        response: Response = None

        if not request.valid:
            response = Response.from_invalid_request(request)
        else:
            method_name = request.method
            method = self.__method_group__.get_method_by_name(method_name)

            if not method:
                response = Response(exception = NoMethodError(method_name), id = request.id)
            elif not params_match_signature(method, request.params):
                response = Response(exception = InvalidParametersError())
            else:
                result = None
                try:
                    if asyncio.iscoroutinefunction(method):
                        result = await call_with_params(method, request.params)
                    else:
                        result = call_with_params(method, request.params)
                except Exception as e:
                    response = Response(exception = e, id = request.id)
                else:
                    response = Response(result = result, id = request.id)

        self._on_response(request, response)
        return response

    def _on_request(self, request: Request) -> None:
        """If present, calls the on_request callback with the provided Request."""

        if self.on_request:
            self.on_request(request)

    def _on_response(self, request: Request, response: Response) -> None:
        """If present, calls the on_response callback with the provided Response."""

        if self.on_response:
            self.on_response(request, response)