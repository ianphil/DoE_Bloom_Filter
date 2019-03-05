#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from bloom_filter.bloom_filter import BloomFilterCalculator

class BloomFilterCalculator_TestSuite(unittest.TestCase):
    """Tests for Bloom Filter Calculator class"""

    def test_false_positive_probability(self):
        calc = BloomFilterCalculator()
        p = calc.false_positive_probability(124, 4, 20)
        assert p == 0.0517

    def test_hash_pass_count(self):
        calc = BloomFilterCalculator()
        k = calc.hash_pass_count(124, 20)
        assert k == 4

    def test_bit_array_size(self):
        calc = BloomFilterCalculator()
        m = calc.bit_array_size(20, 0.05)
        assert m == 124