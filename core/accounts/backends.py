import jwt
import os
from django.shortcuts import get_object_or_404
from django.conf import settings
from rest_framework import authentication, exceptions
from accounts.models import User


def identify(email=None):

    if email:
        return get_object_or_404(User, email=email)


def authenticate_by_refresh_token(token):

    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms="HS256"
        )

        user = User.objects.get(pk=payload['id'])

    except jwt.exceptions.InvalidTokenError as ex:
        raise exceptions.AuthenticationFailed(ex)

    return user


def authenticate_by_password(user, password):
    """Authentication by password"""

    if not user.check_password(password):
        return exceptions.AuthenticationFailed(
            'Password is invalid'
        )

    return user


class CustomAuthentication(authentication.BaseAuthentication):

    def authenticate(self, request):
        """Identification and authentication with request"""

        auth_prefix = os.environ.get("AUTHENTICATION_PREFIX")

        try:
            authorization_header = request.META.get('HTTP_AUTHORIZATION')
            prefix, token = authorization_header.split()
        except:
            return None

        if prefix != auth_prefix:
            return None

        return self._authenticate_by_access_token(token)

    def _authenticate_by_access_token(self, token):

        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms="HS256"
            )

            user = User.objects.get(pk=payload['id'])

        except jwt.exceptions.InvalidTokenError as ex:
            raise exceptions.AuthenticationFailed(ex)

        if not user.is_active:
            raise exceptions.AuthenticationFailed(
                'This user is not active.'
            )

        return user, token

