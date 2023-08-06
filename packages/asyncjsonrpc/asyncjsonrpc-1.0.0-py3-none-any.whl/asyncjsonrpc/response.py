from __future__ import annotations

import json
from typing import Any, Union

from .exceptions import RpcError, InvalidJsonRpcError, JsonDecodeError
from .request import Request

class Response:
    """Describes a JSON-RPC response.

    Attributes:
        result: Result value. May be None. (default: None)
        id: ID of this Response. If not set, this Response will be considered a JSON-RPC
            notification error. (default: None)
    """


    @staticmethod
    def from_json(json_res: str) -> Response:
        """Creates a new Response instance from the provided JSON string.

        If the provided string is not valid JSON or is not JSON-RPC 2.0 compliant, returned Response will have its
        error attribute set to True and its exception attribute set to the relevant RpcError-derived exception.

        Arguments:
            json_res: JSON-RPC response as a JSON string.

        Returns:
            Response: New Response instance.
        """

        try:
            parsed = json.loads(json_res)
        except json.decoder.JSONDecodeError as e:
            return Response(exception = JsonDecodeError(repr(e)))

        return Response.from_dict(parsed)

    @staticmethod
    def from_dict(dict_res: dict) -> Response:
        """Creates a new Response instance from the provided dict.

        If the provided dict is not JSON-RPC 2.0 compliant, returned Response will have its error
        attribute set to True and its exception attribute set to the relevant RpcError-derived exception.

        Arguments:
            dict_res: JSON-RPC response as a dict.

        Returns:
            Response: New Response instance.
        """

        exception = None

        if not 'id' in dict_res:
            exception = InvalidJsonRpcError('"id" property is missing')

        id = dict_res.get('id')
        error = dict_res.get('error')
        if error:
            try:
                exception = RpcError(
                    message = error['message'],
                    code = int(error['code']),
                    data = error.get('data'))
            except TypeError:
                exception = InvalidJsonRpcError('"error" property is not a valid type')
            except KeyError as e:
                exception = InvalidJsonRpcError('"error" property is missing required member "{}"'.format(e.args[0]))

        return Response(
            result = dict_res.get('result'),
            exception = exception,
            id = dict_res.get('id'))

    @staticmethod
    def from_invalid_request(request: Request) -> Response:
        """Creates a new Response from an invalid Request.

        This method is used when an internal JSON-RPC error occurs during the dispatching of a Request. The created
        Response will have an internal flag set marking it as an internal error, causing it to not be marked
        as a notification error even if it doesn't have an ID.

        Arguments:
            request: An invalid Request.

        Raises:
            ValueError: raised if the provided Request is valid.

        Returns:
            The created Response.
        """
        if request.valid:
            raise ValueError('request must not be valid')

        resp = Response(exception = request.exception)
        resp._rpc_error = True
        return resp

    def __init__(self, result: Any = None, exception: Exception = None, id: Union[int, str] = None):
        """Initializes the Response instance.

        Keyword Arguments:
            result: Result value. May be None. (default: None)
            id: ID of this Response. If not set, this Response will be considered a JSON-RPC
                notification error. (default: None)
            exception: Exception of this Response. May be None. (default: None)

        Raises:
            ValueError: When the result and exception arguments are both specified.
        """

        if result and exception:
            raise ValueError('Response cannot be initialized with both result and exception values')

        self.result = result
        self.id = id
        self.exception = exception
        self._rpc_error = False

    @property
    def exception(self) -> Exception:
        """Exception encountered by this Response, if any. When set, also sets the result attribute to None."""

        return self.__exception

    @exception.setter
    def exception(self, exception: Exception):
        self.__exception = exception

        if exception:
            self.result = None

    @property
    def error(self) -> bool:
        """States whether this Response encountered an error. When True, the dict() and json() methods will
        return responses including error data.
        """

        return bool(self.__exception)

    @property
    def error_code(self) -> int:
        """Gets the error code of the current exception if present. If exception inherits from RpcError returns
        the exception's code, on other exceptions returns 0. Returns None if no exception is set.
        """

        if isinstance(self.__exception, RpcError):
            return self.__exception.code
        elif self.__exception:
            return 0

        return None

    @property
    def error_message(self) -> str:
        """Gets the error message of the current exception if present. If exception inherits from RpcError returns
        the exception's message, on other exceptions returns the exception's class's name. Returns None if no
        exception is set.
        """

        if isinstance(self.__exception, RpcError):
            return self.__exception.message
        elif self.__exception:
            return type(self.__exception).__name__

        return None

    @property
    def error_data(self) -> str:
        """Gets the error data of the current exception if present. If exception inherits from RpcError returns
        the exception's data, on other exceptions returns the exception's string representation. Returns None if no
        exception is set.
        """

        if isinstance(self.__exception, RpcError):
            return self.__exception.data
        elif self.__exception:
            return repr(self.__exception)

        return None


    @property
    def notification_error(self) -> bool:
        """States whether this is a response to an error from a JSON-RPC "notification", a request that does not expect
        a response. When True, the dict() and json() methods will return None.
        """

        return self.id == None and not self._rpc_error

    def dict(self) -> dict:
        """Creates a dict containing a JSON-RPC Response object.

        Returns:
            JSON-RPC Response dictionary. Will be None if the notification_error property is True.
        """

        if self.notification_error:
            return None

        out = {'jsonrpc': '2.0', 'id': self.id}
        if self.error:
            out['error'] = {
                'code': int(self.error_code),
                'message': self.error_message,
                'data': self.error_data,
            }
        else:
            out['result'] = self.result

        return out

    def json(self) -> str:
        """Creates a str containing a JSON-RPC Response object as JSON.

        Returns:
            JSON-RPC Response object as a JSON string. Will be None if the notification_error property is True.
        """

        if self.notification_error:
            return None

        return json.dumps(self.dict())