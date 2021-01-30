from rest_framework import mixins, viewsets, status
from accounts.serializers import RegistrationSerializer, ActivationSerializer
from accounts.scripts import decode_token
from accounts.models import User
from rest_framework.response import Response



class RegistrationView(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    serializer_class = RegistrationSerializer

    def create(self, request):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid()
        serializer.save()

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

    serializer_class = ActivationSerializer

    def retrieve(self, request, token):

        try:
            data = decode_token(token)
        except:
            return Response({
                "token": "Invalid token",
                "description" : "Just ensure link is correct or not expired."
          }, status=status.HTTP_400_BAD_REQUEST)

        pk = data.get('pk')
        user = User.objects.get(pk=pk)

        serializer = ActivationSerializer(user, data={'is_active': True}, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({
            'detail': "Your account was successfully activated!"
        })
