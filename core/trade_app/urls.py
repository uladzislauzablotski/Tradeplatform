from rest_framework import routers
from trade_app import views

router = routers.SimpleRouter()
router.register('items', views.ItemViewSet, basename='items')
router.register('watchlist', views.WatchListViewSet, basename='watchlist')
router.register('offers', views.OfferView, basename='offers')
urlpatterns = router.urls
