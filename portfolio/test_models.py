from django.test import TestCase
from portfolio.models import Transaction, Asset
from djmoney.money import Money


class TransacionTestCase(TestCase):
    def setUp(self) -> None:
        Asset.objects.create(ticker="my_ticker")

    def test_update_asset_after_adding_transaction(self):
        cash = Asset.objects.get(ticker='CASH')
        asset = Asset.objects.get(ticker='my_ticker')
        transacton = Transaction.objects.create(
            credit=cash, debit=asset, price=Money(10, 'RUB'), lots=2)
        self.assertEqual(asset.balance, 2)
        self.assertEqual(asset.modified_date, transacton.date)
        self.assertEqual(asset.price, transacton.price)
