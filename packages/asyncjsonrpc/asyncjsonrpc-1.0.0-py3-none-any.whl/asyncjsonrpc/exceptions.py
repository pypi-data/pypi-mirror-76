from typing import Any

class RpcError(Exception):
    """Base exception class for all RPC-related asyncjsonrpc errors.

    Attributes:
        message: Exception's message.
        code: JSON-RPC error code of the exception.
        data: Application-provided data related to the exception.
    """    

    def __init__(self, message: str, code: int = 0, data: Any = None):
        """Initializes an RpcError

        Args:
            message: Exception's message.
            code: JSON-RPC error code of the exception.
            data: Application-provided data related to the exception.
        """

        super().__init__(message)

        self.message = message
        self.code = code
        self.data = data

    def __repr__(self) -> str:
        """Generates a string representation of an RpcError.

        Returns:
            String representation of an RpcError.
        """

        data_str = str(self.data)
        data_truncated = (data_str[:100] + '...') if len(data_str) > 100 else data_str

        return "{type}('{message}', code = {code}, data = {data})".format(
            type = type(self).__name__,
            message = self.message,
            code = self.code,
            data = data_truncated)

class JsonDecodeError(RpcError):
    """Exception indicating that an error was encountered when decoding JSON."""

    def __init__(self, reason: str = None):
        super().__init__('Parse error', code = -32700, data = reason)

class InvalidJsonRpcError(RpcError):
    """Exception indicating that invalid JSON-RPC was encountered."""

    def __init__(self, reason: str = None):
        super().__init__('Invalid Request', code = -32600, data = reason)

class NoMethodError(RpcError):
    """Exception indicatating that a nonexistent method was called."""

    def __init__(self, method_name: str):
        super().__init__('Method not found', code = -32601,
            data = 'No such method "{}"'.format(method_name))

class InvalidParametersError(RpcError):
    """Exception indicating that a method was called with invalid parameters."""

    def __init__(self, reason: str = None):
        super().__init__('Invalid params', code = -32602, data = reason)

class UnexpectedResponseError(Exception):
    """Exception indicating that an unexpected Response was received."""

    pass