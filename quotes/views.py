from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from portfolio.clients.mfd import MfdWebClient
from portfolio.clients.dohod import DohodClient
from portfolio.clients.tbank import TBankClient
from portfolio.clients.bcs import BCSClient
from portfolio.controllers.future_controller import get_quotes
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

mfd = MfdWebClient()
tbank = TBankClient()
dohod_client = DohodClient()
bcs = BCSClient()

def stocks(request):
    quotes = []
    for i in settings.STOCK_TICKERS:
        try:
            quotes.append(tbank.get_last_quote(i))
        except:
            logging.exception(f"Fail to get {i}")
    context = {"quotes": quotes}
    return render(request, "quotes/stocks.html", context)

def bonds(request):
    quotes = []
    for i in settings.BOND_TICKERS:
        try:
            quotes.append(dohod_client.get_last_quote(i))
        except:
            logging.exception(f"Fail to get {i}")
    context = {"quotes": quotes}
    return render(request, "quotes/bonds.html", context)

def futures(request):
    quotes = get_quotes()
    context = {"quotes": quotes}
    return render(request, "quotes/futures.html", context)

def funds(request):
    quotes = []
    for i in settings.FUND_TICKERS:
        try:
            quotes.append(bcs.get_last_quote(i))
        except:
            logging.exception(f"Fail to get {i}")
    context = {"quotes": quotes}
    return render(request, "quotes/funds.html", context)
