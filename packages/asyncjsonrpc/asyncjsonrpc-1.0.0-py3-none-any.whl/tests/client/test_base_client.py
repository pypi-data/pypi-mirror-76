import unittest
import asyncjsonrpc

from ..testutils import asynctest

class TestClient(asyncjsonrpc.client.BaseClient):
    async def _send_request(self, request):
        if request.method == 'a_method':
            response = asyncjsonrpc.Response(
                result = request.params,
                id = request.id)
        else:
            response = asyncjsonrpc.Response(
                exception = asyncjsonrpc.exceptions.RpcError('error'),
                id = request.id)

        self._response_received(response)


class ClientMethodCallTests(unittest.TestCase):
    def setUp(self):
        self.client = TestClient()

    @asynctest
    async def test_method_can_be_called_and_returns_result(self):
        params = (1, 2)
        result = await self.client.a_method(*params)
        self.assertSequenceEqual(params, result)

    @asynctest
    async def test_exceptions_are_raised(self):
        with self.assertRaises(asyncjsonrpc.exceptions.RpcError):
            await self.client.not_a_method()

    @asynctest
    async def test_valueerror_raised_if_positional_and_keyword_arguments_provided(self):
        with self.assertRaises(ValueError):
            await self.client.a_method(1, a = 2)