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

        assert bf.count() == 0

        for i in range(20):
            bf += self.present_users[i]

        self.assertEqual(bf.count(), 62)
        assert bf.count() == 62

    def test_check_bloomfilter(self):
        bf = BloomFilter(124, 4)
        for i in range(20):
            bf += self.present_users[i]

        # TODO: Show Meghan in slide deck as example of bloom
        # This is a present user
        if 'meghan.olson' in bf:
            assert True
        else:
            assert False

        # This is an absent user
        if 'johnny.dang' not in bf:
            assert True
        else:
            assert False

        # This is a false positive
        if 'thanh.vaughn' in bf:
            assert True
        else:
            assert False

        

        