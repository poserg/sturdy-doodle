from django.apps import AppConfig
from django.conf import settings
from .clients.mfd import MfdClient
from .clients.smart_lab import SmartLabClient
from djmoney.money import Money


class PortfolioConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'portfolio'

    def ready(self):
        from .models import AssetType
        try:
            mfd = MfdClient()
            self.upgrade_asset(
                AssetType.STOCK, settings.STOCK_TICKERS, mfd.get_last_quote)
            smart_lab = SmartLabClient()
            self.upgrade_asset(
                AssetType.BOND, settings.BOND_TICKERS,
                smart_lab.retrieve_bond_info)
        except Exception as e:
            print("There was an error: ", e)

    def upgrade_asset(self, type, current_tickers, get_asset):
        from .models import Asset
        exist_tickers = list(
            map(lambda x: x.ticker, Asset.objects.filter(type=type))
        )
        for t in exist_tickers:
            current_tickers.remove(t)

        if len(current_tickers) == 0:
            return
        for i in current_tickers:
            asset_to_add = get_asset(i)
            asset = Asset(ticker=i, name=asset_to_add.name,
                          type=type, price=Money(asset_to_add.price, 'RUB'))
            asset.save()
