#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from src.parsers.montepio_parser import MontepioParser


# python3 -m unittest -v tests/parsers/test_swisscard_parser.py
class MontepioParserTest(unittest.TestCase):
    def test_sample(self):
        transactions = MontepioParser.parse('tests/examples/montepio_example.csv')
        self.assertIsNotNone(transactions)
        self.assertEqual(5, len(transactions))

        self.assertEqual('CHF', transactions[2].currency_code)


if __name__ == '__main__':
    unittest.main()
