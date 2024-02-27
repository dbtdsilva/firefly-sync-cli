#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from src.parsers.bcv_parser import BcvParser

# python3 -m unittest -v tests/parsers/test_swisscard_parser.py
class BcvParserTest(unittest.TestCase):
    def test_sample(self):
        BcvParser.parse('..')
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()