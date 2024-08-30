from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from portfolio.clients.mfd import MfdWebClient
from portfolio.clients.dohod import DohodClient
from portfolio.clients.tbank import TBankClient
from django.conf import settings

mfd = MfdWebClient()
tbank = TBankClient()
dohod_client = DohodClient()

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
