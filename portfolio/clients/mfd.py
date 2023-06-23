# -*- coding: utf-8 -*-

import requests
from datetime import datetime, timedelta
from enum import Enum
import logging
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)

DATE_FORMAT = '%d.%m.%Y'


class Period(Enum):
    MINUTE = 1
    HOUR = 6
    DAY = 7
    MONTH = 9


class Stock:

    def __init__(self, ticker, name, date, price):
        self._ticker = ticker
        self._name = name
        self._date = date
        self._price = price

    @property
    def ticker(self):
        return self._ticker

    @property
    def name(self):
        return self._name

    @property
    def date(self):
        return self._date

    @property
    def price(self):
        return self._price


class MfdClient:

    def __init__(self):
        self.url = "https://mfd.ru/export/handler.ashx/mfdexport.txt"

    def get_last_quote(self, ticker) -> Stock:
        today = datetime.today()
        end = today.strftime(DATE_FORMAT)
        for interval in [(0, Period.HOUR), (1, Period.HOUR), (2, Period.DAY), (5, Period.DAY), (7, Period.DAY)]:
            start = (today-timedelta(days=interval[0])).strftime(DATE_FORMAT)
            quotes = self._get(ticker, start, end, interval[1])
            if len(quotes) != 0:
                break
        if len(quotes) == 0:
            logger.debug(f'Ticker {ticker} does not exist!')
            return Stock(ticker, 'n/a', 'n/a', 'n/a')
        else:
            logger.debug(f'last_line = {quotes[-1]}')
            return self._parse(ticker, quotes[-1])

    def _parse(self, ticker, quote_line):
        line = quote_line.split(';')
        return Stock(ticker, line[0], line[2], line[4])

    def get(self, ticker, start, end, period):
        quotes = self._get(ticker, start, end, period)
        return list(map(lambda x: self._parse(ticker, x), quotes))

    def get_by_year(self, ticker, start, end):
        quotes = self._get(ticker, start, end, Period.MONTH)
        return list(
            filter(
                lambda x: x.date.endswith('1201'),
                map(lambda x: self._parse(ticker, x), quotes)))

    def _get(self, ticker, start, end, period):
        response = requests.get(
            self.url,
            params={
                'TickerGroup': '11',
                'Tickers': f'{ticker}',
                'Alias': 'false',
                'Period': f'{period.value}',
                'timeframeValue': '1',
                'timeframeDatePart': 'day',
                'StartDate': f'{start}',
                'EndDate': f'{end}',
                'SaveFormat': '0',
                'SaveMode': '0',
                'FileName': 'mfdexport.txt',
                'FieldSeparator': '%3b',
                'DecimalSeparator': '.',
                'DateFormat': 'yyyyMMdd',
                'TimeFormat': 'HHmmss',
                'DateFormatCustom': '',
                'TimeFormatCustom': '',
                'AddHeader': 'false',
                'RecordFormat': '2',
                'Fill': 'false'
            },)
        return [line for line in response.text.split('\n')
                if line.strip() != '']


class MfdWebClient:
    def __init__(self):
        self.url = "https://m.mfd.ru/marketdata/ticker"

    def get_last_quote(self, ticker) -> Stock:
        html = self._get(ticker)
        return self._parse(ticker, html)

    def _parse(self, ticker, html):
        return Stock(
            ticker,
            html.find(
                "h1").text.strip(),
            html.find("div", class_="m-companytable-time").text,
            html.find("div", class_="m-companytable-last")
                .text
                .replace(" ", ""))

    def _get(self, ticker):
        response = requests.get(
            self.url,
            params={
                'id': f'{ticker}'
            })
        soap = BeautifulSoup(response.text, 'html.parser')
        return soap
