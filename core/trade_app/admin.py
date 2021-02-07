from django.contrib import admin
from trade_app.models import Currency, Item

@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    pass

@admin.register(Item)
class CurrencyAdmin(admin.ModelAdmin):
    pass