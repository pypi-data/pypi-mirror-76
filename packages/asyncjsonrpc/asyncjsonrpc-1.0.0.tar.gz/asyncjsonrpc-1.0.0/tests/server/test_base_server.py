import unittest
import asyncjsonrpc.server

from ..testutils import req, asynctest

# TODO per spec, must handle arrays of requests. hmm could be tricky with this setup. maybe a MultiRequest class? or make Request.from_json return an array?
# oh and responses to a batch must be batched too, so yup looks like MultiRequest and MultiResponse it is. tricky.
# actually call them RequestBatch and ResponseBatch

def test_methods_group():
    group = asyncjsonrpc.MethodGroup()

    @group.method
    def no_args():
        return

    @group.method
    def two_positional_args(a, b):
        return a, b

    @group.method
    def any_positional_args(*args):
        return args

    @group.method
    def specific_keyword_args(a = None, b = None):
        return {'a': a, 'b': b}

    @group.method
    def any_keyword_args(**kwargs):
        return kwargs

    return group


class PositionalAndKeywordArgumentsTests(unittest.TestCase):
    def setUp(self):
        self.test_server = asyncjsonrpc.server.BaseServer(method_group = test_methods_group())

    @asynctest
    async def test_no_args_are_passed(self):
        resp = await self.test_server._dispatch_request(req('no_args'))
        self.assertIsNone(resp.exception)
        self.assertFalse(resp.error)

    @asynctest
    async def test_correct_number_of_positional_args_are_passed(self):
        args = (1, 2)
        resp = await self.test_server._dispatch_request(req('two_positional_args', *args))
        self.assertIsNone(resp.exception)
        self.assertSequenceEqual(args, resp.result)

    @asynctest
    async def test_incorrect_number_of_positional_args_raises_exception(self):
        args = (1, 2, 3)
        resp = await self.test_server._dispatch_request(req('two_positional_args', *args))
        self.assertIsInstance(resp.exception, asyncjsonrpc.exceptions.InvalidParametersError)

    @asynctest
    async def test_any_number_of_positional_args_are_passed(self):
        args = (1, 2, 3, 4, 5)
        resp = await self.test_server._dispatch_request(req('any_positional_args', *args))
        self.assertIsNone(resp.exception)
        self.assertSequenceEqual(args, resp.result)

    @asynctest
    async def test_specific_keyword_args_are_passed(self):
        kwargs = {'a': 1, 'b': 2}
        resp = await self.test_server._dispatch_request(req('specific_keyword_args', **kwargs))
        self.assertIsNone(resp.exception)
        self.assertDictEqual(kwargs, resp.result)

    @asynctest
    async def test_incorrect_keyword_args_raises_exception(self):
        kwargs = {'a': 1, 'b': 2, 'c': 3}
        resp = await self.test_server._dispatch_request(req('specific_keyword_args', **kwargs))
        self.assertIsInstance(resp.exception, asyncjsonrpc.exceptions.InvalidParametersError)

    @asynctest
    async def test_any_keyword_args_are_passed(self):
        kwargs = {'a': 1, 'b': 2, 'c': 3, 'd': 4, 'e': 5}
        resp = await self.test_server._dispatch_request(req('any_keyword_args', **kwargs))
        self.assertIsNone(resp.exception)
        self.assertDictEqual(kwargs, resp.result)