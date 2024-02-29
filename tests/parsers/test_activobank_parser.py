#!/usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
from src.parsers.activo_bank_parser import ActivoBankParser


# python3 -m unittest -v tests/parsers/test_swisscard_parser.py
class ActivoBankParserParser(unittest.TestCase):
    def test_sample(self):
        transactions = ActivoBankParser.parse('tests/examples/activo_bank_mov.xlsx')
        self.assertIsNotNone(transactions)
        self.assertEqual(8, len(transactions))


if __name__ == '__main__':
    unittest.main()
