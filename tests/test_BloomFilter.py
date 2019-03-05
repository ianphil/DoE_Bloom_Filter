#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from src.model.bloom_filter import BloomFilter
from src.model.users import PresentUsers, AbsentUsers

class BloomFilter_TestSuite(unittest.TestCase):
    """Tests for Bloom Filter class"""

    @classmethod
    def setUpClass(self):
        self.present_users = PresentUsers('./src/resources/present.txt')
        self.absent_users = AbsentUsers('./src/resources/absent.txt')

    def test_add_bloomfilter(self):
        bf = BloomFilter(124, 4)

        self.assertEqual(bf.count(), 0)

        for i in range(20):
            bf += self.present_users[i]

        self.assertEqual(bf.count(), 62)

    def test_check_bloomfilter(self):
        bf = BloomFilter(124, 4)
        for i in range(20):
            bf += self.present_users[i]

        # TODO: Show Meghan in slide deck as example of bloom
        # This is a present user
        self.assertTrue('meghan.olson' in bf, msg='Present user expected')

        # This is an absent user
        self.assertFalse('johnny.dang' in bf, msg='Absent user not expected')

        # This is a false positive
        self.assertTrue('thanh.vaughn' in bf, msg='False positive for user expected')

        

        