import unittest
import json
import asyncjsonrpc

class RequestInitializerTests(unittest.TestCase):
    method = 'test'
    params = [1, 2, 3]
    id = 123
    req_dict = {'jsonrpc': '2.0', 'method': method, 'params': params, 'id': id}

    def test_request_can_be_initialized_with_json_string(self):
        req_string = json.dumps(self.req_dict)
        req = asyncjsonrpc.Request.from_json(req_string)

        self.assertTrue(req.valid)
        self.assertEqual(self.method, req.method)
        self.assertSequenceEqual(self.params, req.params)
        self.assertEqual(self.id, req.id)

    def test_request_can_be_initialized_with_dict(self):
        req = asyncjsonrpc.Request.from_dict(self.req_dict)

        self.assertTrue(req.valid)
        self.assertEqual(self.method, req.method)
        self.assertSequenceEqual(self.params, req.params)
        self.assertEqual(self.id, req.id)

    def test_request_marked_invalid_on_invalid_json(self):
        invalid = 'this is invalid json'

        req = asyncjsonrpc.Request.from_json(invalid)
        self.assertFalse(req.valid)
        self.assertIsInstance(req.exception, asyncjsonrpc.exceptions.JsonDecodeError)

    def test_request_marked_invalid_on_missing_method_property(self):
        invalid_req_dic = dict(self.req_dict)
        del invalid_req_dic['method']

        req = asyncjsonrpc.Request.from_dict(invalid_req_dic)
        self.assertFalse(req.valid)
        self.assertIsInstance(req.exception, asyncjsonrpc.exceptions.InvalidJsonRpcError)


class RequestToJsonRpcTests(unittest.TestCase):
    expected = {
        'jsonrpc': '2.0',
        'id': 123,
        'method': 'method',
        'params': [1, 2, 3],
    }

    def test_dict_returns_jsonrpc_request(self):
        req = asyncjsonrpc.Request('method', params = [1, 2, 3], id = 123)
        self.assertDictEqual(self.expected, req.dict())

    def test_dict_on_notification_returns_jsonrpc_request_without_id(self):
        expected = dict(self.expected)
        del expected['id']

        req = asyncjsonrpc.Request('method', params = [1, 2, 3])
        self.assertTrue(req.notification)
        self.assertDictEqual(expected, req.dict())

    def test_dict_on_no_params_returns_jsonrpc_request_without_params(self):
        expected = dict(self.expected)
        del expected['params']

        req = asyncjsonrpc.Request('method', id = 123)
        self.assertDictEqual(expected, req.dict())

    def test_json_returns_jsonrpc_json_string(self):
        req = asyncjsonrpc.Request('method', params = [1, 2, 3], id = 123)
        self.assertDictEqual(self.expected, json.loads(req.json()))

    def test_dict_raises_exception_on_invalid(self):
        req = asyncjsonrpc.Request(exception = Exception())
        self.assertFalse(req.valid)

        with self.assertRaises(ValueError):
            req.dict()