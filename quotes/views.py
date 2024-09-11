from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from portfolio.clients.mfd import MfdWebClient
from portfolio.clients.dohod import DohodClient
from portfolio.clients.tbank import TBankClient
from portfolio.clients.tbank_futures import TBankFuturesClient
from django.conf import settings

mfd = MfdWebClient()
tbank = TBankClient()
dohod_client = DohodClient()
tbank_futures_client = TBankFuturesClient()

def stocks(request):
    quotes = []
    for i in settings.STOCK_TICKERS:
        quotes.append(tbank.get_last_quote(i))
    context = {"quotes": quotes}
    return render(request, "quotes/stocks.html", context)

def bonds(request):
    quotes = []
    for i in settings.BOND_TICKERS:
        quotes.append(dohod_client.get_last_quote(i))
    context = {"quotes": quotes}
    return render(request, "quotes/bonds.html", context)

def futures(request):
    quotes = sorted(tbank_futures_client.get_quotes(), key=lambda x: x.basic_asset)
    context = {"quotes": quotes}
    return render(request, "quotes/futures.html", context)
