# Generated by Django 4.1.3 on 2022-11-17 03:09

from django.db import migrations
from portfolio.models import AssetType


def forward_func(apps, schema_editor):
    Asset = apps.get_model("portfolio", "Asset")
    cash = Asset(ticker="CASH", name="Cash", type=AssetType.CASH)
    cash.save()


def reverse_func(apps, schema_editor):
    Asset = apps.get_model("portfolio", "Asset")
    db_alias = schema_editor.connection.alias
    Asset.objects.using(db_alias).filter(ticker='CASH').delete()


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio', '0005_asset_price_asset_price_currency'),
    ]

    operations = [
        migrations.RunPython(forward_func, reverse_func)
    ]
