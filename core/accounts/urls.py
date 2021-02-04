from django.urls import path
from rest_framework import routers
from accounts import views

router = routers.SimpleRouter()
router.register('signup', views.RegistrationView, basename='signup')
router.register('activate', views.ActivationView, basename='activate')
router.register('login', views.LogInView, basename='login')
router.register('access_token', views.AccessTokenView, basename='access_token')
urlpatterns = router.urls
