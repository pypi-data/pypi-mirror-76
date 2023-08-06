import unittest
import asyncjsonrpc

class MethodGroupAddRemoveTests(unittest.TestCase):
    def setUp(self):
        self.group = asyncjsonrpc.MethodGroup()

    def a_method(self): pass

    def test_add_method_adds_method_to_group_by_method_name(self):
        self.group.add_method(self.a_method)
        self.assertEqual(self.a_method, self.group.get_method_by_name(self.a_method.__name__))

    def test_add_method_adds_method_to_group_by_specified_name(self):
        self.group.add_method(self.a_method, name = 'method_name')
        self.assertEqual(self.a_method, self.group.get_method_by_name('method_name'))

    def test_remove_method_removes_method_from_group_by_method_name(self):
        self.group.add_method(self.a_method)
        self.assertEqual(self.a_method, self.group.get_method_by_name(self.a_method.__name__))

        self.group.remove_method(self.a_method)
        self.assertIsNone(self.group.get_method_by_name(self.a_method.__name__))

    def test_remove_method_removes_method_from_group_by_specified_name(self):
        self.group.add_method(self.a_method, name = 'method_name')
        self.assertEqual(self.a_method, self.group.get_method_by_name('method_name'))

        self.group.remove_method('method_name')
        self.assertIsNone(self.group.get_method_by_name('method_name'))


class MethodGroupDecoratorTests(unittest.TestCase):
    def setUp(self):
        self.group = asyncjsonrpc.MethodGroup()

        @self.group.method
        def a_method():
            return 'a_method'

        self.a_method = a_method

    def test_method_decorator_adds_method_to_group_by_method_name(self):
        got_method = self.group.get_method_by_name('a_method')
        self.assertEqual(self.a_method(), got_method())