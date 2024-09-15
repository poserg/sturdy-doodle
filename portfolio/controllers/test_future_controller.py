# -*- coding: utf-8 -*-

import unittest

from portfolio.clients.tbank_futures import TBankFuturesClient, Future
from portfolio.controllers.future_controller import get_futures_by_basic_asset, calc_delta, get_quotes
from unittest.mock import patch, MagicMock
import logging


class TestFutureController(unittest.TestCase):
    def setUp(self):
        logging.basicConfig(level=logging.DEBUG)
        logging.getLogger().setLevel(logging.DEBUG)
        self.client = TBankFuturesClient()

    @patch('portfolio.clients.tbank_futures.requests')
    @patch('portfolio.controllers.future_controller.client')
    def test_get_futures(self, mock_client, mock_requests):
        mock_response = MagicMock()
        with open('portfolio/clients/fixture_tbank_futures.json', 'r') as f:
            mock_response.text = f.read()
        mock_requests.post.return_value = mock_response

        mock_client.get_quotes.return_value = self.client.get_quotes()

        result = get_futures_by_basic_asset()
        self.assertIn('Commodity', result)
        self.assertIn('NG', result['Commodity'])
        self.assertIn('NGX4', result['Commodity']['NG'])

    def test_calc_delta(self):
        result = calc_delta({
            'NGU4': Future('NGU4', 'name1', 'NG', 'Commodity', 16, 2.167),
            'NGV4': Future('NGV4', 'name2', 'NG', 'Commodity', 49, 2.536),
            'NGX4': Future('NGX4', 'name3', 'NG', 'Commodity', 77, 3.027),
            'NGZ4': Future('NGZ4', 'name4', 'NG', 'Commodity', 108, 3.29),
        })

        self.assertEqual(result[:5], [
            ['Asset', 'NGU4', 'NGV4', 'NGX4', 'NGZ4'],
            ['Days', 16, 49, 77, 108],
            ['Price', 2.167, 2.536, 3.027, 3.29],
            ['NGU4', '0.000', '-0.369', '-0.860', '-1.123'],
            ['NGV4', '0.369', '0.000', '-0.491', '-0.754'],
        ])

    @patch('portfolio.clients.tbank_futures.requests')
    @patch('portfolio.controllers.future_controller.client')
    def test_get_quotes(self, mock_client, mock_requests):
        mock_response = MagicMock()
        with open('portfolio/clients/fixture_tbank_futures.json', 'r') as f:
            mock_response.text = f.read()
        mock_requests.post.return_value = mock_response

        mock_client.get_quotes.return_value = self.client.get_quotes()

        result = get_quotes()
        self.assertEqual(result[0].name, 'Commodity')
        self.assertEqual(result[0].values[0].name, 'Brent')
        self.assertIn('BRV4', result[0].values[0].values[0])
