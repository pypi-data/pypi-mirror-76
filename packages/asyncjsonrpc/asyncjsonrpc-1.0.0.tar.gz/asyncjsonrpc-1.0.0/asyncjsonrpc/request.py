from __future__ import annotations

import json
from typing import Union

from .exceptions import RpcError, JsonDecodeError, InvalidJsonRpcError

class Request:
    """Describes a JSON-RPC request.

    Attributes:
        method: Name of the method this Request calls. May be None if the Request is not valid.
        params: This Request's method arguments, either as a list of positional arguments or
            dictionary of keyword arguments. (default: None)
        id: ID of this Request. If not set, this Request will be considered a JSON-RPC
            notification. (default: None)
        exception: Exception that occurred during the creation of this Request. If set, request will
            be considered not valid. (default: None)
        valid: States whether this is a valid Request. Invalid Requests will have the reason for their
            invalidation in the exception attribute.
    """

    @staticmethod
    def from_json(json_req: str) -> Request:
        """Creates a new Request instance from the provided JSON string.

        If the provided string is not valid JSON or is not JSON-RPC 2.0 compliant, returned Request will have its
        error attribute set to True and its exception attribute set to the relevant RpcError-derived exception.

        Arguments:
            json_req: JSON-RPC request as a JSON string.

        Returns:
            Request: New Request instance.
        """

        try:
            parsed = json.loads(json_req)
        except json.decoder.JSONDecodeError as e:
            return Request(exception = JsonDecodeError(repr(e)))

        return Request.from_dict(parsed)

    @staticmethod
    def from_dict(dict_req: dict) -> Request:
        """Creates a new Request instance from the provided dict.

        If the provided dict is not JSON-RPC 2.0 compliant, returned Request will have its error
        attribute set to True and its exception attribute set to the relevant RpcError-derived exception.

        Arguments:
            dict_req: JSON-RPC request as a dict.

        Returns:
            Request: New Request instance.
        """

        error_reason = None

        if not dict_req.get('method'):
            error_reason = '"method" property is missing'
        elif not type(dict_req.get('params')) in (list, dict, type(None)):
            error_reason = 'Invalid value for "params" property'

        if error_reason:
            return Request(exception = InvalidJsonRpcError(error_reason))

        return Request(
            method = dict_req.get('method'),
            params = dict_req.get('params'),
            id = dict_req.get('id'))

    def __init__(
        self,
        method: str = None,
        params: Union[list, dict] = None,
        id: Union[int, str] = None,
        exception: RpcError = None):
        """Initializes a new Request instance.

        Keyword Arguments:
            method: Name of the method this Request calls. Must be specified unless the exception argument
                is set. (default: None)
            params: This Request's method arguments, either as a list of positional arguments or
                dictionary of keyword arguments. (default: None)
            id: ID of this Request. (default: None)
            exception: Exception that occurred during the creation of this Request. (default: None)

        Raises:
            ValueError: Neither the method nor the exception parameter were set.
        """

        if not method and not exception:
            raise ValueError('Request must be initialized with a request or exception value')

        self.method = method
        self.params = params
        self.id = id

        self.valid = exception == None
        self.exception = exception

    @property
    def notification(self) -> bool:
        """States whether this request is a JSON-RPC "notification", a request that does not expect a response."""
        return self.id == None

    def dict(self) -> dict:
        """Creates a dict containing a JSON-RPC Request object.

        Raises:
            ValueError: raised if called on an invalid Request.

        Returns:
            JSON-RPC Request object.
        """

        if not self.valid:
            raise ValueError('cannot create request dict from invalid Request')

        out = {
            'jsonrpc': '2.0',
            'method': self.method,
        }

        if self.id:
            out['id'] = self.id
        if self.params:
            out['params'] = self.params

        return out

    def json(self) -> str:
        """Creates a string containing a JSON-RPC Request object as JSON.

        Raises:
            ValueError: raised if called on an invalid Request.

        Returns:
            JSON-RPC Request object as JSON.
        """

        if not self.valid:
            raise ValueError('cannot create request string from invalid Request')

        return json.dumps(self.dict())