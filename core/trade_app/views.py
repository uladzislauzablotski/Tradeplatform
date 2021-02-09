from rest_framework import mixins, viewsets
from trade_app.serializers import (ItemSerializer, WatchListSerializer, WatchListCreateItemSerializer, OfferSerializer,
                                   InventorySerializer)
from trade_app.models import (Item, WatchList, Offer)
from rest_framework.response import Response
from rest_framework.permissions import AllowAny


class ItemViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()


class WatchListViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    def get_serializer_class(self):
        if self.action == 'create':
            return WatchListCreateItemSerializer

        return WatchListSerializer

    def create(self, request):
        user = self.request.user
        watchlist = WatchList.objects.get(user=user)

        items = WatchListCreateItemSerializer(watchlist, data=request.data)
        items.is_valid(raise_exception=True)

        items.save(owner=self.request.user)

        return Response(request.data)

    def destroy(self, request, pk):
        user = self.request.user
        watchlist = WatchList.objects.get(user=user)

        watchlist.items.remove(pk)

        return Response(request.data)

    def get_queryset(self):

        user = self.request.user

        watchlist = WatchList.objects.get(user=user)

        """get items from user's watchlist"""
        return watchlist.items.all()


class OfferView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = OfferSerializer

    def get_queryset(self):
        return Offer.objects.filter(user=self.request.user).order_by('created_at')

    def create(self, request):
        user = self.request.user

        offer = self.serializer_class(data=request.data)
        offer.is_valid(raise_exception=True)

        offer.save(user=user)

        return Response(offer.data)


class InventoryView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):

    serializer_class = InventorySerializer

    def get_queryset(self):
        return self.request.user.inventory.all()




