# -*- coding: utf-8 -*-

import requests
from datetime import datetime, timedelta
from enum import Enum
import logging


logger = logging.getLogger(__name__)

DATE_FORMAT = '%d.%m.%Y'


class Period(Enum):
    MINUTE = 1
    HOUR = 6
    MONTH = 9


class MfdClient:

    def __init__(self):
        self.url = "https://mfd.ru/export/handler.ashx/mfdexport.txt"

    def get_last_quote(self, ticker):
        today = datetime.today()
        end = today.strftime(DATE_FORMAT)
        start = (today-timedelta(days=7)).strftime(DATE_FORMAT)
        quotes = self._get(ticker, start, end, Period.MINUTE)
        last_line = quotes[-1].split(';')
        logger.debug(f'last_line = {last_line}')
        return last_line[2], last_line[4]

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
        return [line for line in response.text.split('\r\n')
                if line.strip() != '']
