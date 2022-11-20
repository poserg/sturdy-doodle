from django.contrib import admin
from .models import Asset, Transaction


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ("ticker", "name", "balance",
                    "shares_in_lot", "type", "modified_date")
    readonly_fields = [
        'ticker',
        'balance',
        'name',
        'price',
        'type',
        'modified_date',
    ]


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("date", "debit", "price")
