#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from src.parsers.bcv_parser import BcvParser

# python3 -m unittest -v tests/parsers/test_swisscard_parser.py
class BcvParserTest(unittest.TestCase):
    def test_sample(self):
        transactions = BcvParser.parse('tests/examples/BCV-TRANSACTIONS_21-02-2024.xlsx')
        self.assertIsNotNone(transactions)
        self.assertEqual(7, len(transactions))

if __name__ == '__main__':
    unittest.main()