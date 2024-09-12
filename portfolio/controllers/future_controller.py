from portfolio.clients.tbank_futures import TBankFuturesClient

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