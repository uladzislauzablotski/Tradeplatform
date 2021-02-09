from rest_framework import serializers
from trade_app.models import Item, WatchList, Offer, Inventory, Price


class ItemSerializer(serializers.ModelSerializer):

    price = serializers.IntegerField(source='price.value')

    class Meta:
        model = Item
        fields = ('code', 'name', 'price', 'currency')

    def create(self, validated_data):

        item = Item.objects.create(**validated_data)
        Price.objects.create(item=item)
        print('hello')

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

        action = data.get('action')
        user = data.get('user')
        item = data.get('item')
        amount = data.get('amount')

        "If action is sell"
        if not action:
            try:
                user_has = user.inventory.get(item=item).amount

                if not user_has >= amount:
                    raise Exception

            except Exception:
                raise serializers.ValidationError({
                    'amount': 'You have no {amount} stocks of {name_of_stock}'.format(
                        amount=amount, name_of_stock=item.name
                    )
                })

        return Offer.objects.create(**validated_data)


class InventorySerializer(serializers.ModelSerializer):

    item = ItemSerializer()

    class Meta:
        model = Inventory
        fields = ('item', 'amount',)