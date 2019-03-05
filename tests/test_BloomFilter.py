#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from bloom_filter.bloom_filter import BloomFilter
from bloom_filter.users import PresentUsers, AbsentUsers

class BloomFilter_TestSuite(unittest.TestCase):
    """Tests for Bloom Filter class"""

    @classmethod
    def setUpClass(self):
        self.present_users = PresentUsers('./bloom_filter/resources/present.txt')
        self.absent_users = AbsentUsers('./bloom_filter/resources/absent.txt')

    def test_add_bloomfilter(self):
        bf = BloomFilter(124, 4)
        for i in range(20):
            bf.add(self.present_users[i])
        assert bf.bit_array.count() == 58
        