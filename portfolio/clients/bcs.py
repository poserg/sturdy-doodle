# -*- coding: utf-8 -*-

import requests
import logging
from portfolio.clients.mfd import Stock
import json


logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.DEBUG)


class BCSClient:

    def __init__(self):
        self.url = "https://api.bcs.ru/udfdatafeed/v1/search/group?limit=1&search="

    def get_last_quote(self, ticker) -> Stock:
        html = self._get(ticker)
        return self._parse(html, ticker)

    def _parse(self, html, ticker):
        logger.debug(html)
        data = json.loads(html)
        return Stock(
            ticker,
            data["data"][0]["instruments"][0]["shortName"],
            None,
            data["data"][0]["instruments"][0]["closePrice"]
            )

    def _get(self, ticker):
        response = requests.get(self.url + ticker)
        return response.text