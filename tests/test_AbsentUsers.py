#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from bloom_filter.users import AbsentUsers

class AbsentUsers_TestSuite(unittest.TestCase):
    """Tests for Absent Users class"""

    def test_Absent_Users(self):
        absent_users = AbsentUsers('./bloom_filter/resources/absent.txt')
        assert len(absent_users) == 1000