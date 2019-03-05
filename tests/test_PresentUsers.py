#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from src.model.users import PresentUsers

class PresentUsers_TestSuite(unittest.TestCase):
    """Tests for Present Users class"""

    def test_Present_Users(self):
        present_users = PresentUsers('./src/resources/present.txt')
        self.assertEqual(len(present_users), 10000)