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

    amount = models.PositiveSmallIntegerField(
        blank=False
    )

    price = models.FloatField(
        blank=False,
        validators=[validate_price]
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE
    )
