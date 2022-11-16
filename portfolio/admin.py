from django.contrib import admin
from .models import Asset, Transaction


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ("ticker", "name", "lots", "shares_in_lot", "type")


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("date", "debit", "price")
