import os
from django.db import transaction
from accounts.signals import user_created
from django.dispatch import receiver
from trade_app.models import (Currency, WatchList, Account)


@transaction.atomic
@receiver(user_created)
def user_created(sender, instance, **kwargs):

    """Created user should have one Account with default currency"""

    currency, created = Currency.objects.get_or_create(
        code=os.environ.get("DEFAULT_CURRENCY_CODE", "USD"),
        defaults={'name': os.environ.get("DEFAULT_CURRENCY_NAME", "DEFAULT_CURRENCY_NAME")}
    )

    Account.objects.create(
        user=instance,
        currency=currency
    )

    WatchList.objects.create(user=instance)