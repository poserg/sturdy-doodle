# -*- coding: utf-8 -*-

import unittest

from main.mfd import MfdClient

class Mfd(unittest.TestCase):

	def test_get_last_quote(self):
		client = MfdClient()
		date, price = client.get_last_quote(1464)
		self.assertRegex(date, '[0-9]{8}')
		self.assertRegex(price, '^[0-9]+(\.[0-9]+)?$')