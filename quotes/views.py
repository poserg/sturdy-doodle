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
logging.basicConfig(level=logging.DEBUG)

mfd = MfdWebClient()
tbank = TBankClient()
dohod_client = DohodClient()
bcs = BCSClient()

def stocks(request):
    quotes = get_stocks(settings.STOCK_TICKERS)
    context = {"quotes": quotes}
    return render(request, "quotes/stocks.html", context)

def get_stocks(tickers):
    quotes = []
    for i in tickers:
        try:
            quotes.append(tbank.get_last_quote(i))
        except:
            logging.exception(f"Fail to get {i}")
    return quotes

def bonds(request):
    quotes = get_bonds(settings.BOND_TICKERS)
    context = {"quotes": quotes}
    return render(request, "quotes/bonds.html", context)

def get_bonds(tickers):
    quotes = []
    for i in tickers:
        try:
            quotes.append(dohod_client.get_last_quote(i))
        except:
            logging.exception(f"Fail to get {i}")
    return quotes


def futures(request):
    quotes = get_quotes()
    context = {"quotes": quotes}
    return render(request, "quotes/futures.html", context)

def funds(request):
    quotes = get_funds(settings.FUND_TICKERS)
    context = {"quotes": quotes}
    return render(request, "quotes/funds.html", context)

def get_funds(tickers):
    quotes = []
    for i in tickers:
        try:
            quotes.append(bcs.get_last_quote(i))
        except:
            logging.exception(f"Fail to get {i}")
    return quotes

def common_request(request):
    stock_tickers = request.GET.getlist("stock", '')
    stocks = get_stocks(stock_tickers)
    
    bonds_ticker = request.GET.getlist("bond", '')
    logger.debug(f"bonds_ticker = {bonds_ticker}")
    bonds = get_bonds(bonds_ticker)
    
    funds_ticker = request.GET.getlist("fund", '')
    logger.debug(f"funds_ticker = {funds_ticker}")
    funds = get_funds(funds_ticker)

    context = {
        "stocks": stocks,
        "bonds": bonds,
        "funds": funds,
    }
    return render(request, "quotes/common.html", context)