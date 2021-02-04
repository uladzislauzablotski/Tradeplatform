from rest_framework import serializers
from accounts.models import User
from accounts.backends import identify
from accounts.backends import authenticate_by_refresh_token, authenticate_by_password


class RegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        allow_blank=False,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password',)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class ActivationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('is_active',)

    def update(self, instance, validated_data):
        instance.is_active = validated_data.get('is_active')
        instance.save()

        return instance


class LogInSerializer(serializers.Serializer):

    email = serializers.EmailField(
        allow_blank=False,
    )

    password = serializers.CharField(
        style={'input_type': 'password'},
        allow_blank=False,
    )

    def validate(self, data):

        email = data.get('email')
        password = data.get('password')

        """Identification"""
        user = identify(email=email)

        """Authentication"""
        authenticate_by_password(user, password=password)

        return user.get_tokens()


class AccessTokenSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(
        max_length=250,
        allow_blank=False
    )

    def validate_refresh_token(self, value):

        """Authentication"""
        user = authenticate_by_refresh_token(value)

        return user.get_tokens()
