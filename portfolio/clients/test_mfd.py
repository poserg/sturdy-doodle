# -*- coding: utf-8 -*-

import unittest

from portfolio.clients.mfd import MfdClient
# import logging


class Mfd(unittest.TestCase):
    # def setUp(self):
    #   logging.basicConfig(level=logging.DEBUG)
    #   logging.getLogger().setLevel(logging.DEBUG)

    def test_get_last_quote(self):
        client = MfdClient()
        stock = client.get_last_quote('1464')
        self.assertEqual(stock.name, 'Сбербанк-п')
        self.assertEqual(stock.ticker, '1464')
        self.assertRegex(stock.date, '[0-9]{8}')
        self.assertRegex(stock.price, '^[0-9]+(.[0-9]+)?$')
