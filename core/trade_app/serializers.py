from rest_framework import serializers
from trade_app.models import (Item, WatchList, Offer, Inventory, Price, Account, Currency)
from trade_app.scripts import start_rezervation


class ItemSerializer(serializers.ModelSerializer):
    price = serializers.IntegerField(source='price.value')

    class Meta:
        model = Item
        fields = ('code', 'name', 'price', 'currency')

    def create(self, validated_data):
        item = Item.objects.create(**validated_data)
        Price.objects.create(item=item)

        return item


class WatchListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class WatchListCreateItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchList
        fields = ('items',)

    def update(self, watchlist, validated_data):

        user = dict(**validated_data).get('owner')
        items = dict(**validated_data).get('items')

        for item in items:
            try:
                user.watchlist.get(items=item)
            except Exception:
                raise serializers.ValidationError(
                    {"item": "Item is already exists in watchlist",
                     'id': item.id
                     }
                )

            watchlist.items.add(item)

        return watchlist


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ('amount', 'price', 'item', 'action', 'created_at')

    def create(self, validated_data):
        data = dict(**validated_data)

        start_rezervation(data)

        return Offer.objects.create(**validated_data)


class InventorySerializer(serializers.ModelSerializer):
    item = ItemSerializer()

    class Meta:
        model = Inventory
        fields = ('item', 'amount', 'reserved_amount')


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class AccountSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer()

    class Meta:
        model = Account
        fields = ('currency', 'balance', 'reserved_balance')


class AccountCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ('currency',)
