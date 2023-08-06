import unittest
import json

import asyncjsonrpc
from .testutils import req


class ResponseInitializerTests(unittest.TestCase):
    # TODO add tests and code for creating Response from JSON and dict
    # also, maybe remove error_code et al attrs and just use RpcError values? that's how Server methods
    # will set error codes anyway, not much use case for setting them on the Response object directly
    # and that'd be pretty ugly

    def test_initializer_sets_result_and_id(self):
        result = 'result'
        id = 1
        resp = asyncjsonrpc.Response(result, id = id)
        self.assertEqual(result, resp.result)
        self.assertEqual(id, resp.id)

    def test_initializer_sets_exception_and_id(self):
        exception = Exception()
        id = 1
        resp = asyncjsonrpc.Response(exception = exception, id = 1)
        self.assertIs(exception, resp.exception)
        self.assertEqual(id, resp.id)

    def test_initializer_raises_exception_on_result_and_exception(self):
        with self.assertRaises(ValueError):
            asyncjsonrpc.Response(result = 1, exception = Exception())


class ExceptionSetterTests(unittest.TestCase):
    def test_exception_setter_sets_error_to_true_when_exception_present(self):
        resp = asyncjsonrpc.Response(exception = Exception())
        self.assertTrue(resp.error)

    def test_exception_setter_sets_error_to_false_when_exception_not_present(self):
        resp = asyncjsonrpc.Response()
        self.assertFalse(resp.error)

    def test_exception_setter_sets_error_attrs_for_non_RpcError(self):
        exception = Exception('test')
        resp = asyncjsonrpc.Response(exception = exception)
        self.assertEqual(Exception.__name__, resp.error_message)
        self.assertEqual(0, resp.error_code)
        self.assertEqual(repr(exception), resp.error_data)

    def test_exception_setter_sets_error_attrs_for_RpcError(self):
        exception = asyncjsonrpc.exceptions.RpcError(message = 'test', code = 123, data = 'data')
        resp = asyncjsonrpc.Response(exception = exception)
        self.assertEqual(exception.message, resp.error_message)
        self.assertEqual(exception.code, resp.error_code)
        self.assertEqual(exception.data, resp.error_data)


class NotificationErrorGetterTests(unittest.TestCase):
    def test_notification_error_is_true_on_no_id(self):
        resp = asyncjsonrpc.Response(id = None)
        self.assertTrue(resp.notification_error)

    def test_notification_error_is_false_on_id(self):
        resp = asyncjsonrpc.Response(id = 123)
        self.assertFalse(resp.notification_error)

    def test_notificaiton_error_is_false_on_response_from_invalid_request(self):
        req = asyncjsonrpc.Request(exception = asyncjsonrpc.exceptions.JsonDecodeError)
        self.assertFalse(req.valid)

        resp = asyncjsonrpc.Response.from_invalid_request(req)
        self.assertTrue(resp._rpc_error)
        self.assertFalse(resp.notification_error)


class ResponseToJsonRpcTests(unittest.TestCase):
    expected = {
        'jsonrpc': '2.0',
        'id': 123,
        'result': 'result',
    }

    error_expected = {
        'jsonrpc': '2.0',
        'id': 123,
        'error': {
            'code': 234,
            'message': 'message',
            'data': 'data',
        },
    }

    def test_dict_returns_jsonrpc_response(self):
        resp = asyncjsonrpc.Response('result', id = 123)
        self.assertDictEqual(self.expected, resp.dict())

    def test_dict_returns_jsonrpc_error_response(self):
        exception = asyncjsonrpc.exceptions.RpcError('message', 234, 'data')
        resp = asyncjsonrpc.Response(exception = exception, id = 123)
        self.assertDictEqual(self.error_expected, resp.dict())

    def test_json_returns_jsonrpc_json_string(self):
        resp = asyncjsonrpc.Response('result', id = 123)
        self.assertEqual(json.dumps(self.expected), resp.json())

    def test_dict_returns_none_on_notification_error(self):
        resp = asyncjsonrpc.Response('result')
        self.assertTrue(resp.notification_error)
        self.assertIsNone(resp.dict())


class ResponseFromJsonRpcTests(unittest.TestCase):
    expected = {
        'jsonrpc': '2.0',
        'id': 123,
        'result': 'result',
    }

    error_expected = {
        'jsonrpc': '2.0',
        'id': 123,
        'error': {
            'code': 234,
            'message': 'message',
            'data': 'data',
        },
    }

    def test_from_dict_returns_response(self):
        resp = asyncjsonrpc.Response.from_dict(self.expected)
        self.assertEqual(self.expected['result'], resp.result)

    def test_from_dict_with_error_returns_error_response(self):
        resp = asyncjsonrpc.Response.from_dict(self.error_expected)

        self.assertTrue(resp.error)
        self.assertEqual(self.error_expected['error']['code'], resp.error_code)

    def test_from_json_returns_response(self):
        json_resp = json.dumps(self.expected)
        resp = asyncjsonrpc.Response.from_json(json_resp)

        self.assertEqual(self.expected['result'], resp.result)

    def test_from_json_with_error_returns_error_response(self):
        json_resp = json.dumps(self.error_expected)
        resp = asyncjsonrpc.Response.from_json(json_resp)

        self.assertTrue(resp.error)
        self.assertEqual(self.error_expected['error']['code'], resp.error_code)