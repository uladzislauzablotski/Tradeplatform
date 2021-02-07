from django.db.models.signals import post_save
from accounts.signals import user_created
from django.dispatch import receiver
from trade_app.models import Item, Price, WatchList


@receiver(post_save, sender=Item)
def my_handler(sender, instance, **kwargs):
    Price.objects.create(value=0, item=instance)


@receiver(user_created)
def my_handler(sender, instance, **kwargs):
    WatchList.objects.create(user=instance)