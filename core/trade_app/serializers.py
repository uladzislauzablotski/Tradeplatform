from rest_framework import serializers
from django.db import transaction
from trade_app.models import (Item, WatchList, Offer, Inventory, Price, Account, Currency)
from trade_app.scripts import Reservation


class ItemSerializer(serializers.ModelSerializer):
    price = serializers.IntegerField(source='price.value')

    class Meta:
        model = Item
        fields = ('code', 'name', 'price', 'currency')

    @transaction.atomic
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
        user = validated_data.get('user')
        items = validated_data.get('items')

        request_items = tuple(map(lambda x: x.id, items))

        # we have only one item in queryset
        db_items = tuple(user.watchlist.items.values_list('id', flat=True))

        already_in_watchlist = [i for i in request_items if i in db_items]

        if already_in_watchlist:
            raise serializers.ValidationError(dict(
                items=already_in_watchlist,
                detail="Items are already in watchlist"
            ))

        # one request to add multiple items
        user.watchlist.items.add(*items)

        return validated_data


class OfferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Offer
        fields = ('amount', 'price', 'item', 'action', 'created_at')

    @transaction.atomic
    def create(self, validated_data):

        Reservation.start_reservation(validated_data)

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
