import unittest
from unittest.mock import patch, MagicMock
from portfolio.clients.smart_lab import SmartLabClient


class SmartLabTest(unittest.TestCase):
    @patch('portfolio.clients.smart_lab.requests')
    def test_retrieve_bond(self, mock_requests):
        mock_response = MagicMock()
        mock_response.status_code = 200
        with open('portfolio/clients/smart_lab_response.html', 'r') as f:
            mock_response.text = f.read()
        mock_requests.get.return_value = mock_response

        client = SmartLabClient()
        bond = client.retrieve_bond_info('SU26215RMFS2')
        self.assertEqual(bond.price, 99.747)
        self.assertEqual(bond.oid, 15.72)
        self.assertEqual(bond.name, 'ОФЗ 26215')
