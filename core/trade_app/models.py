from django.conf import settings
from django.db import models
from trade_app.validators import validate_price


class StockBase(models.Model):
    code = models.CharField(max_length=10,
                            unique=True,
                            blank=False,)

    name = models.CharField(max_length=30)

    def __str__(self):
        return self.code

    class Meta:
        abstract = True


class Currency(StockBase):
    class Meta:
        verbose_name = 'Currency'
        verbose_name_plural = 'Currencies'


class Item(StockBase):
    currency = models.ForeignKey(
        Currency,
        related_name='+',
        on_delete=models.PROTECT,
        blank=False
    )


class Price(models.Model):
    value = models.FloatField(
        max_length=15,
        default=0

    )

    item = models.OneToOneField(
        Item,
        related_name='price',
        on_delete=models.CASCADE,
        blank=False
    )


class WatchList(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='watchlist',
        blank=False
    )

    items = models.ManyToManyField(
        Item
    )


class TradeBase(models.Model):
    price = models.FloatField(
        blank=False,
        validators=[validate_price]
    )

    amount = models.PositiveIntegerField(
        blank=False
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        abstract = True


class Offer(models.Model):
    item = models.ForeignKey(
        Item,
        related_name='+',
        blank=False,
        on_delete=models.CASCADE
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='offers',
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


class Trade(models.Model):
    item = models.ForeignKey(
        Item,
        related_name='+',
        blank=False,
        on_delete=models.SET_NULL(),
        null=True,
    )

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
