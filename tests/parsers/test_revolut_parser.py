#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from src.parsers.revolut_parser import RevolutParser


# python3 -m unittest -v tests/parsers/test_swisscard_parser.py
class RevolutParserTest(unittest.TestCase):
    def test_sample(self):
        transactions = RevolutParser.parse('tests/examples/revolut_example.csv')
        self.assertIsNotNone(transactions)
        self.assertEqual(9, len(transactions))


if __name__ == '__main__':
    unittest.main()
