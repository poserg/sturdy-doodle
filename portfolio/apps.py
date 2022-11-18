from django.apps import AppConfig
from django.conf import settings
from .clients.mfd import MfdClient
from djmoney.money import Money


class PortfolioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'portfolio'

    def ready(self):
        from .models import AssetType
        try:
            self.upgrade_asset(AssetType.STOCK, settings.STOCK_TICKERS)
        except Exception as e:
            print("There was an error: ", e)

    def upgrade_asset(self, type, current_tickers):
        from .models import Asset
        exist_tickers = list(
            map(lambda x: x.ticker, Asset.objects.filter(type=type))
        )
        for t in exist_tickers:
            current_tickers.remove(t)

        if len(current_tickers) == 0:
            return
        mfd = MfdClient()
        for i in current_tickers:
            stock = mfd.get_last_quote(i)
            asset = Asset(ticker=i, name=stock.name,
                          type=type, price=Money(stock.price, 'RUB'))
            asset.save()
