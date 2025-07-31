from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from portfolio.clients.mfd import MfdWebClient
from portfolio.clients.dohod import DohodClient
from portfolio.clients.tbank import TBankClient
from portfolio.clients.bcs import BCSClient
from portfolio.controllers.future_controller import get_quotes
from django.conf import settings

mfd = MfdWebClient()
tbank = TBankClient()
dohod_client = DohodClient()
bcs = BCSClient()

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
    quotes = get_quotes()
    context = {"quotes": quotes}
    return render(request, "quotes/futures.html", context)

def funds(request):
    quotes = []
    for i in settings.FUND_TICKERS:
        quotes.append(bcs.get_last_quote(i))
    context = {"quotes": quotes}
    return render(request, "quotes/funds.html", context)
