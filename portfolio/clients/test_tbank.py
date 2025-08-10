# -*- coding: utf-8 -*-

import unittest

from portfolio.clients.tbank import TBankClient
from unittest.mock import patch, MagicMock
import logging


class TBankTest(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger().setLevel(logging.DEBUG)
        self.client = TBankClient()

    @patch('portfolio.clients.tbank.requests')
    def test_get_quotes(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        with open('portfolio/clients/fixture_tbank_quote.json', 'r') as f:
            mock_response.text = f.read()
        mock_requests.post.return_value = mock_response

        stock = self.client.get_last_quote("SBER")
        self.assertEqual(stock.ticker, 'SBER')
        self.assertEqual(stock.name, 'Сбербанк')
        self.assertEqual(stock.date, '2025-08-10T12:48:29.00556+03:00')
        self.assertEqual(stock.price, 317.97)
