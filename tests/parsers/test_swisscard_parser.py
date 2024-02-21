#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from src.parsers.swisscard_parser import SwisscardCsv

# python3 -m unittest -v tests/parsers/test_swisscard_parser.py
class SwisscardParserTest(unittest.TestCase):
    def test_sample(self):
        SwisscardCsv.parse_csv('tests/examples/SC-Transactions_2024-02-21_20-31-02.csv')
        self.assertTrue(True)

if __name__ == '__main__':
    unittest.main()