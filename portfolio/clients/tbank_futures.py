# -*- coding: utf-8 -*-

import requests
import logging
import json


logger = logging.getLogger(__name__)
# logging.basicConfig(level=logging.DEBUG)


class TBankFuturesClient:

    def __init__(self):
        self.url = "https://www.tbank.ru/api/trading/futures/list"

    def get_quotes(self):
        html = self._get()
        return self._parse(html)

    def _parse(self, html):
        logger.debug(html)
        data = json.loads(html)
        items = data["payload"]["values"]

        result = []
        for item in items:
            result.append(Future(
                item["instrumentInfo"]["ticker"],
                item["viewInfo"]["showName"],
                item["instrumentInfo"]["basicAsset"],
                item["instrumentInfo"]["basicAssetType"],
                item["instrumentInfo"]["daysTillLastTrade"],
                item["priceInfo"]["last"] if "last" in item["priceInfo"] else None
                ))
        return result


    def _get(self):
        response = requests.post(
            self.url,
            json = {
                "start":"0",
                "end":"1000",
                "orderType":"Desc",
                "sortType":"ByCumulativePrice"
            }
            )
        return response.text

class Future:

    def __init__(self, ticker, name, basic_asset, basic_asset_type, days_till_last_trade, price):
        self._ticker = ticker
        self._name = name
        self._basic_asset = basic_asset
        self._basic_asset_type = basic_asset_type
        self._days_till_last_trade = days_till_last_trade
        self._price = price

    @property
    def name(self):
        return self._name

    @property
    def ticker(self):
        return self._ticker

    @property
    def basic_asset(self):
        return self._basic_asset

    @property
    def basic_asset_type(self):
        return self._basic_asset_type

    @property
    def days_till_last_trade(self):
        return self._days_till_last_trade

    @property
    def price(self):
        return self._price

    def __repr__(self):
        return f"<Future ticker:{self.ticker}, basic_asset:{self.basic_asset}, price:{self.price}>"
