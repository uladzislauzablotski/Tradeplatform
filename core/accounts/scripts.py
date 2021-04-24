import jwt
from django.conf import settings
from rest_framework.response import Response


def get_domain():
    return 'http://localhost:8081'


def generate_token(**kwargs):

    token = jwt.encode(
        kwargs,
        settings.SECRET_KEY,
        algorithm="HS256"
    )

    return token


def decode_token(token):

    data = jwt.decode(
        token,
        settings.SECRET_KEY,
        algorithms=["HS256"]
    )

    return data


