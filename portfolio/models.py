from django.db import models
from djmoney.models.fields import MoneyField
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone


class AssetType(models.TextChoices):
    BOND = 'BOND', _('Bond')
    STOCK = 'STOCK', _('Stock')
    CASH = 'CASH', _('Cash')

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

    def __str__(self):
        return self.name


class Asset(models.Model):
    ticker = models.CharField(max_length=20, primary_key=True)
    name = models.CharField(max_length=200)
    type = models.CharField(max_length=20, choices=AssetType.choices)
    balance = models.BigIntegerField(default=0)
    shares_in_lot = models.BigIntegerField(default=1)
    price = MoneyField(max_digits=14, decimal_places=6,
                       default_currency='RUB', default=0)
    modified_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.name} ({self.ticker}:{self.type})"


class Transaction(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    credit = models.ForeignKey(
        Asset, on_delete=models.PROTECT, related_name='credit')
    debit = models.ForeignKey(
        Asset, on_delete=models.PROTECT, related_name='debit')
    price = MoneyField(max_digits=14, decimal_places=6, default_currency='RUB')
    lots = models.BigIntegerField(default=0)

    def __str__(self):
        return f"Transaction({self.date.date()}: " + \
                f"credit={self.credit.ticker}, " + \
                f"debit={self.debit.ticker}, " + \
                f"price={self.price!r})"


@receiver(post_save, sender=Transaction, dispatch_uid="update_balance")
def update_balance(sender, instance, **kwargs):
    instance.debit.balance += instance.lots
    instance.debit.modified_date = instance.date
    instance.debit.price = instance.price
    instance.debit.save()
