from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render
from portfolio.clients.mfd import MfdWebClient
from django.conf import settings

mfd = MfdWebClient()

def index(request):
    # for i in tickers:
    stocks = []
    for i in settings.STOCK_TICKERS:
        stocks.append(mfd.get_last_quote(i))
    context = {"quotes": stocks}
    return render(request, "quotes/index.html", context)