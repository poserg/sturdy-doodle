# -*- coding: utf-8 -*-

import requests
from datetime import datetime, timedelta
import logging
logger = logging.getLogger(__name__)

tickers = [1464]

DATE_FORMAT = '%d.%m.%Y'


class MfdClient:

	def __init__(self):
		# self.url = "https://mfd.ru/export/handler.ashx/mfdexport_1month_17102006_17102022.txt?TickerGroup=11&Tickers={ticker}&Alias=false&Period=9&timeframeValue=1&timeframeDatePart=day&StartDate={start}&EndDate={end}&SaveFormat=0&SaveMode=0&FileName=mfdexport_1month_{ticker}.txt&FieldSeparator=%3b&DecimalSeparator=.&DateFormat=yyyyMMdd&TimeFormat=HHmmss&DateFormatCustom=&TimeFormatCustom=&AddHeader=true&RecordFormat=2&Fill=false"
		self.url = "https://mfd.ru/export/handler.ashx/mfdexport_1month_17102006_17102022.txt?TickerGroup=11&Tickers={ticker}&Alias=false&Period={period}&timeframeValue=1&timeframeDatePart=day&StartDate={start}&EndDate={end}&SaveFormat=0&SaveMode=0&FileName=mfdexport_1month_{ticker}.txt&FieldSeparator=%3b&DecimalSeparator=.&DateFormat=yyyyMMdd&TimeFormat=HHmmss&DateFormatCustom=&TimeFormatCustom=&AddHeader=true&RecordFormat=2&Fill=false"

	def get_last_quote(self, ticker):
		today = datetime.today()
		end = today.strftime(DATE_FORMAT)
		start = (today-timedelta(days=7)).strftime(DATE_FORMAT)
		quotes=self._get(ticker, start, end, 1)
		last_line=quotes[-1].split(';')
		logger.debug(f'last_line = {last_line}')
		return last_line[2], last_line[4]

	def _get(self, ticker, start, end, period):
		u = self.url.format(ticker=ticker, start=start, end=end, period=period)
		logger.debug(f"url = {u}")
		response = requests.get(u)
		return [line for line in response.text.split('\r\n') if line.strip() != '']
		
