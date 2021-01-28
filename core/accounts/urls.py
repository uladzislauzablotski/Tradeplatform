from django.urls import path
from rest_framework import routers

from accounts import views

router = routers.SimpleRouter()
router.register('signup', views.RegistrationView, basename='signup')
urlpatterns = router.urls
