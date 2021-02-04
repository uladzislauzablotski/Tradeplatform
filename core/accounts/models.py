import jwt
from django.db import models
from accounts.managers import UserManager
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from accounts.scripts import generate_token
from datetime import datetime, timedelta
from accounts.scripts import decode_token, generate_token
from rest_framework import exceptions


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model.
    """

    username = models.CharField(
        db_index=True,
        max_length=255,
        unique=True,
        blank=False
    )

    email = models.EmailField(
        unique=True,
        blank=False,
        )

    def __str__(self):
        return self.username

    is_staff = models.BooleanField(default=False)

    is_active = models.BooleanField(default=False)

    refresh_token = models.CharField(max_length=255)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ('username',)

    objects = UserManager()

    def get_tokens(self):

        self.refresh_token = self._generate_refresh_token()

        return {
            'access_token': self._generate_access_token(),
            'refresh_token': self._generate_refresh_token()
        }

    def _generate_access_token(self):

        dt = datetime.now() + timedelta(days=1)

        token = generate_token(
            id=self.pk,
            type="access",
            exp=dt.strftime('%s')
        )

        return token

    def _generate_refresh_token(self):

        dt = datetime.now() + timedelta(days=5)

        token = generate_token(
            id=self.pk,
            type="refresh",
            exp=dt.strftime('%s')
        )

        """
        As there is only valid refresh_token,
        we should keep it on backend side.
        """
        self.refresh_token = token
        self.save()

        return token

