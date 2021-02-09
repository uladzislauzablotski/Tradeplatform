from rest_framework import mixins, viewsets, status, authentication
from rest_framework.permissions import AllowAny
from .serializers import (RegistrationSerializer, ActivationSerializer, LogInSerializer, AccessTokenSerializer)
from accounts.scripts import decode_token
from accounts.models import User
from rest_framework.response import Response



class RegistrationView(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def create(self, request):

        serializer = self.serializer_class(data=request.data)

        serializer.is_valid(raise_exception=True)

        serializer.save()
        data = {
            "message": "We've send confirmation link on your email."
                       " In oder to activate account click the link in the message."
        }

        return Response(data, status=status.HTTP_201_CREATED)


#Not Ok
class ActivationView(
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet
):
    lookup_field = 'token'
    lookup_value_regex = '[\w\.-]+'

    permission_classes = (AllowAny,)
    serializer_class = ActivationSerializer

    def retrieve(self, request, token):

        try:
            data = decode_token(token)
            pk = data.get('pk')
            user = User.objects.get(pk=pk)
        except:
            return Response({
                "token": "Invalid token",
                "description" : "Just ensure link is correct or not expired."
          }, status=status.HTTP_400_BAD_REQUEST)

        serializer = ActivationSerializer(user, data={'is_active': True}, partial=True)

        serializer.is_valid(raise_exception=True)

        serializer.save()

        return Response({
            'detail': "Your account was successfully activated!"
        })

#OK
class LogInView(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (AllowAny,)
    serializer_class = LogInSerializer

    def create(self, request):

        serializer = LogInSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        return Response(
            serializer.validated_data
        )

#
class AccessTokenView(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    permission_classes = (AllowAny,)
    serializer_class = AccessTokenSerializer

    def create(self, request):
        serializer = AccessTokenSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        return Response(
            serializer.validated_data
        )

