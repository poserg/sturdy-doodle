from django.contrib import admin
from .models import Asset, Transaction


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'name',
                    'price',
                    'balance',
                    'shares_in_lot', 'type',
                    'modified_date')
    readonly_fields = [
        'ticker',
        'balance',
        'name',
        'price',
        'type',
        'modified_date',
    ]

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("date", "debit", "price")

    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False
