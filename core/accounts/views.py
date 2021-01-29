from rest_framework import mixins, viewsets
from accounts.serializers import RegistrationSerializer
from rest_framework.response import Response
from django.contrib.auth.models import User


class RegistrationView(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = RegistrationSerializer

    def create(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()

        if not serializer.save():
            data = serializer.errors

        data = {
            "message": "We've send confirmation link on your email."
                       " In oder to activate account click the link in the message."
        }

        return Response(data)



class ActivationView(
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    lookup_field = 'token'
    lookup_value_regex = '[\w\.-]+'

    def retrieve(self, request, token):
        print(token)
        return Response(request.data)
