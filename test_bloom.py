#!/usr/bin/env python
import unittest
import bloom

class BloomTest(unittest.TestCase):
    def test_fun(self):
        self.assertEqual(bloom.fun(3), 4)

if __name__ == '__main__':
    unittest.main()