from rest_framework import serializers
from accounts.models import User


class RegistrationSerializer(serializers.ModelSerializer):


    password = serializers.CharField(
        max_length=128,
        min_length=8,
        allow_blank=False,
        style={'input_type': 'password'}
    )

    class Meta:
        model = User
        fields = ('email', 'username', 'password', )

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