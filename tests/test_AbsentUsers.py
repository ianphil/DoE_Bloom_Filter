#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from src.model.users import AbsentUsers

class AbsentUsers_TestSuite(unittest.TestCase):
    """Tests for Absent Users class"""

    def test_Absent_Users(self):
        absent_users = AbsentUsers('./src/resources/absent.txt')
        self.assertEqual(len(absent_users), 1000)