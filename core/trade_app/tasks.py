from tradeplatform.celery import app
from django.shortcuts import get_object_or_404
from .models import Offer, Trade, Inventory


@app.task
def make_trades(*args, **kwargs):
    buy_offers = Offer.objects.filter(action=True).order_by('created_at')

    for buy_offer in buy_offers:

        while True:

            next = find_suitable_sell_offer_and_make_trade(buy_offer)

            if not next:
                "There is no suitable offer" \
                "or there is no more need in to find offers for buyer"
                break


def find_suitable_sell_offer_and_make_trade(buy_offer):
    sell_offer = find_sell_offer_suitable_for_buy_price(buy_offer.price)

    if not sell_offer:
        "If there is no suitable offer"
        return None

    return make_trade(buy_offer, sell_offer)


def make_trade(buy_offer, sell_offer):
    amount_to_buy = buy_offer.amount
    amount_to_sell = sell_offer.amount

    if amount_to_buy > amount_to_sell:
        return trade_amount_to_buy_more(buy_offer, sell_offer, amount_to_sell)

    elif amount_to_buy < amount_to_sell:
        return trade_amount_to_buy_less(buy_offer, sell_offer, amount_to_buy)

    elif amount_to_buy == amount_to_sell:
        return trade_amount_to_buy_equal(buy_offer, sell_offer, amount_to_buy)


def trade_amount_to_buy_more(buy_offer, sell_offer, amount):
    buy_offer.amount = buy_offer.amount + amount
    buy_offer.save()

    change_buyer_inventory(buy_offer)
    change_seller_inventory(sell_offer, amount)

    create_trade(buy_offer, sell_offer, amount)

    sell_offer.delete()

    return True


def trade_amount_to_buy_less(buy_offer, sell_offer, amount):
    sell_offer.amount = sell_offer.amount - amount
    sell_offer.save()

    change_buyer_inventory(buy_offer)
    change_seller_inventory(sell_offer, amount)

    create_trade(buy_offer, sell_offer, amount)

    buy_offer.delete()

    """There is no more need to find offers for this buy-offer"""
    return False


def trade_amount_to_buy_equal(buy_offer, sell_offer, amount):
    change_buyer_inventory(buy_offer)
    change_seller_inventory(sell_offer)

    create_trade(buy_offer, sell_offer, amount)

    sell_offer.delete()
    buy_offer.delete()

    """There is no more need to find offers for this buy-offer"""
    return False


def change_buyer_inventory(buy_offer):
    user = buy_offer.user
    item = buy_offer.item
    amount = buy_offer.amount

    inventory, created = Inventory.objects.filter(item=item).get_or_create(
        user=user,
        defaults={
            'item': item
        }
    )

    inventory_amount = inventory.amount
    inventory.amount = inventory_amount + amount

    inventory.save()


def change_seller_inventory(sell_offer, amount):
    user = sell_offer.user
    item = sell_offer.item

    inventory = get_object_or_404(Inventory.objects.filter(item=item), user=user)

    inventory_amount = inventory.amount
    inventory.amount = inventory_amount - amount

    inventory.save()


def find_sell_offer_suitable_for_buy_price(price):
    return Offer.objects.filter(
        action=False,
        price__lte=price
    ).first()


def create_trade(buy_offer, sell_offer, amount):
    return Trade.objects.create(
        buyer=buy_offer.user,
        seller=sell_offer.user,
        item=buy_offer.item,
        amount=amount,
        price=sell_offer.price
    )
