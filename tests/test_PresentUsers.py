#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from bloom_filter.users import PresentUsers

class PresentUsers_TestSuite(unittest.TestCase):
    """Tests for Present Users class"""

    def test_Present_Users(self):
        present_users = PresentUsers('./bloom_filter/resources/present.txt')
        assert len(present_users) == 10000