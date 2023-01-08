# -*- coding: utf-8 -*-

import unittest

from portfolio.clients.mfd import MfdClient
from unittest.mock import patch, MagicMock
import logging


class Mfd(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger().setLevel(logging.DEBUG)
        self.client = MfdClient()

    @patch('portfolio.clients.mfd.requests')
    def test_get_last_quote(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = 'Сбербанк-п;1;20230106;234900;140.12;10'
        mock_requests.get.return_value = mock_response

        stock = self.client.get_last_quote('1464')
        self.assertEqual(stock.name, 'Сбербанк-п')
        self.assertEqual(stock.ticker, '1464')
        self.assertEqual(stock.date, '20230106')
        self.assertEqual(stock.price, '140.12')

    @patch('portfolio.clients.mfd.requests')
    def test_get_last_quote_with_empty_response(self, mock_requests):
        mock_requests.get.text.return_value = ''

        stock = self.client.get_last_quote('1464')
        self.assertEqual(stock.price, 'n/a')
