from unittest import TestCase
from stack import Stack

class TestStack(TestCase):

    def setUp(self) -> None:
        self.stack = Stack()
    
    def tearDown(self) -> None:
        self.stack = None

    def test_is_empty(self):
        self.assertTrue(self.stack.is_empty())

    def test_pop(self):
        self.assertIsNone(self.stack.pop())
        self.stack.push(4)
        self.stack.push(2)
        self.assertEqual(self.stack.pop(), 2)
        self.assertEqual(self.stack.pop(), 4)
        self.assertIsNone(self.stack.pop())
    
    def test_push(self):
        self.stack.push(1)
        self.assertEqual(self.stack.peek(), 1)
        self.stack.push(2)
        self.assertEqual(self.stack.pop(), 2)
    
    def test_peek(self):
        self.stack.push(1)
        self.stack.push(2)
        self.assertEqual(self.stack.peek(), 2)
        self.stack.pop()
        self.stack.pop()
        self.assertIsNone(self.stack.peek())
    