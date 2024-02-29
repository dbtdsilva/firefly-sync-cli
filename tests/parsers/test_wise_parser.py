#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from src.parsers.wise_parser import WiseParser


# python3 -m unittest -v tests/parsers/test_swisscard_parser.py
class WiseParserTest(unittest.TestCase):
    def test_sample(self):
        transactions = WiseParser.parse('tests/examples/wise_example.csv')
        self.assertIsNotNone(transactions)
        self.assertEqual(9, len(transactions))


if __name__ == '__main__':
    unittest.main()
