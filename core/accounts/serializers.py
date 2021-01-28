from rest_framework import serializers
from accounts.models import User


class RegistrationSerializer(serializers.Serializer):

    username = serializers.CharField()
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password'}
    )

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)