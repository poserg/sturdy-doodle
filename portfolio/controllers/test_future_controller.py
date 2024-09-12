# -*- coding: utf-8 -*-

import unittest

from portfolio.clients.tbank_futures import TBankFuturesClient
from portfolio.controllers.future_controller import get_futures_by_basic_asset
from unittest.mock import patch, MagicMock
import logging


class TestFutureController(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger().setLevel(logging.DEBUG)
        self.client = TBankFuturesClient()

    @patch('portfolio.clients.tbank_futures.requests')
    @patch('portfolio.controllers.future_controller.client')
    def test_get_quotes(self, mock_client, mock_requests):
        mock_response = MagicMock()
        with open('portfolio/clients/fixture_tbank_futures.json', 'r') as f:
            mock_response.text = f.read()
        mock_requests.post.return_value = mock_response

        mock_client.get_quotes.return_value = self.client.get_quotes()

        result = get_futures_by_basic_asset()
        self.assertIn('Commodity', result)
        self.assertIn('NG', result['Commodity'])
        self.assertIn('NGX4', result['Commodity']['NG'])
