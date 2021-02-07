from rest_framework import serializers
from trade_app.models import Item, WatchList


class ItemSerializer(serializers.ModelSerializer):

    class Meta:
        model = Item
        fields = '__all__'


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
            if WatchList.objects.filter(user=user, items=item).exists():

                raise serializers.ValidationError(
                    {"item": "Item is already exists in watchlist",
                     'id': item.id
                     }
                )

            watchlist.items.add(item)

        return watchlist