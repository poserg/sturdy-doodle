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
			column_price = Decimal(column.price) if column.price else Decimal(0)
			row_price = Decimal(row.price) if row.price else Decimal(0)
			line.append("{:2.3f}".format(row_price - column_price))
	return result

def get_quotes():
	futures = get_futures_by_basic_asset()
	result = {}
	for asset_type in futures.keys():
		t = {}
		result[asset_type] = t
		for basic_asset in futures[asset_type].keys():
			t[basic_asset] = calc_delta(futures[asset_type][basic_asset])
	return result