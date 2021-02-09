from django.conf import settings
from django.db import models
from trade_app.validators import validate_price


class Currency(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=20)

    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'

    def __str__(self):
        return self.code


class Item(models.Model):
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=20)

    currency = models.ForeignKey(
        Currency,
        related_name='+',
        on_delete=models.PROTECT
    )

    def __str__(self):
        return self.code


class Price(models.Model):
    value = models.FloatField(
        max_length=15,

    )

    item = models.OneToOneField(
        Item,
        related_name='price',
        on_delete=models.CASCADE
    )


class WatchList(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    items = models.ManyToManyField(
        Item,
    )


class Offer(models.Model):

    amount = models.PositiveIntegerField(
        blank=False
    )

    price = models.FloatField(
        blank=False,
        validators=[validate_price]
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
        on_delete=models.CASCADE
    )

    item = models.ForeignKey(
        Item,
        blank=False,
        on_delete=models.CASCADE
    )

    '''
    There are only to actions :
    Buy or Sell
    '''
    action = models.BooleanField(
        blank=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )


class Trade(models.Model):
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='buy',
        blank=False,
    )

    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
        related_name='sell',
        on_delete=models.CASCADE
    )

    item = models.ForeignKey(
        Item,
        blank=False,
        on_delete=models.CASCADE
    )

    amount = models.PositiveIntegerField(
        blank=False
    )

    price = models.FloatField(
        blank=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )


class Inventory(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        blank=False,
        related_name='inventory',
        on_delete=models.CASCADE
    )

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='+',
        blank=False
    )

    amount = models.PositiveIntegerField(
        blank=False,
        default=0
    )
