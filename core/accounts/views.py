from rest_framework import mixins, viewsets
from accounts.serializers import RegistrationSerializer
from django.contrib.auth.models import User


class RegistrationView(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = RegistrationSerializer