# -*- coding: utf-8 -*-

import requests
import logging
from portfolio.clients.mfd import Stock
import json


logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.DEBUG)


class TBankClient:

    def __init__(self):
        self.url = "https://www.tbank.ru/api/trading/stocks/get"

    def get_last_quote(self, ticker) -> Stock:
        html = self._get(ticker)
        return self._parse(html, ticker)

    def _parse(self, html, ticker):
        logger.debug(html)
        data = json.loads(html)
        return Stock(
            ticker,
            data["payload"]["symbol"]["brand"],
            data["time"],
            data["payload"]["prices"]["last"]["value"]
            )

    def _get(self, ticker):
        response = requests.post(
            self.url,
            json = {
                "ticker": ticker
            }
            )
        return response.text