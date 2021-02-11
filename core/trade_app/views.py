from rest_framework import mixins, viewsets
from trade_app.serializers import (ItemSerializer, WatchListSerializer, WatchListCreateItemSerializer, OfferSerializer,
                                   InventorySerializer, AccountSerializer, AccountCreateSerializer)
from trade_app.models import (Item, WatchList, Offer, Account)
from rest_framework.response import Response


class ItemViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = ItemSerializer

    def get_queryset(self):
        return Item.objects.select_related('price').all()


class WatchListViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet
):
    serializers = {
        'create': WatchListCreateItemSerializer,
        'list': WatchListSerializer
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, 'list')

    def create(self, request):
        user = self.request.user

        items = self.get_serializer(user.watchlist, data=request.data)
        items.is_valid(raise_exception=True)

        items.save(user=self.request.user)

        return Response(items.data)

    def destroy(self, request, pk):
        user = self.request.user

        removed_user = user.watchlist.items.remove(pk)

        return Response(removed_user)

    def get_queryset(self):
        user = self.request.user

        """get items from user's watchlist"""
        return user.watchlist.items.all()


class OfferView(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = OfferSerializer

    def get_queryset(self):
        return self.request.user.offers.all().order_by('created_at')

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


class AccountView(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializers = {
        'create': AccountCreateSerializer,
        'list': AccountSerializer
    }

    def get_serializer_class(self):
        return self.serializers.get(self.action, 'list')

    def get_queryset(self):
        return self.request.user.accounts.all()