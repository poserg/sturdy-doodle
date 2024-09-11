# -*- coding: utf-8 -*-

import unittest

from portfolio.clients.tbank_futures import TBankFuturesClient
from unittest.mock import patch, MagicMock
import logging


class TBankFuturesTest(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger().setLevel(logging.DEBUG)
        self.client = TBankFuturesClient()

    @patch('portfolio.clients.tbank_futures.requests')
    def test_get_quotes(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        with open('portfolio/clients/fixture_tbank_futures.json', 'r') as f:
            mock_response.text = f.read()
        mock_requests.post.return_value = mock_response

        stock = self.client.get_quotes()[0]
        self.assertEqual(stock.ticker, 'NGU4')
        self.assertEqual(stock.basic_asset, 'NG')
        self.assertEqual(stock.basic_asset_type, 'Commodity')
        self.assertEqual(stock.days_till_last_trade, 16)
        self.assertEqual(stock.price, 2.167)
