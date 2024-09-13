from portfolio.clients.tbank_futures import TBankFuturesClient
from decimal import *

client = TBankFuturesClient()

def get_futures_by_basic_asset():
	quotes = client.get_quotes()
	result = {}
	for q in quotes:
		if q.basic_asset_type in result:
			t = result[q.basic_asset_type]
		else:
			t = {}
			result[q.basic_asset_type] = t
		if q.basic_asset in t:
			asset = t[q.basic_asset]
		else:
			asset = {}
			t[q.basic_asset] = asset
		asset[q.ticker] = q
	return result

def calc_delta(futures):
	items = sorted(futures.values(), key=lambda kv: kv.days_till_last_trade)
	result = [['Asset'] + [k.ticker for k in items]]
	for row in items:
		line = [row.ticker]
		result.append(line)
		for column in items:
			line.append("{:2.3f}".format(Decimal(row.price) - Decimal(column.price)))
	return result