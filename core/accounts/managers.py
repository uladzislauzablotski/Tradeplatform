from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):

    def _create_user(self, username, email, password, **extra_fields):

        if not username:
            raise ValueError("Username is required!")

        if not email:
            raise ValueError("Email is required!")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_user(self, username, email, password, **extra_fields):

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):

        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)

        if extra_fields.get('is_staff') is not True:
            raise ValueError("is_staff for superuser should bet True!")

        if extra_fields.get('is_superuser') is not True:
            raise ValueError("is_superuser for superuser should bet True!")

        return self._create_user(username, email, password, **extra_fields)