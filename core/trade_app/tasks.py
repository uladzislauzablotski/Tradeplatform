from tradeplatform.celery import app
from .models import Offer, Trade


@app.task
def make_trades(*args, **kwargs):
    buy_offers = Offer.objects.filter(action=True).order_by('created_at')

    for buy_offer in buy_offers:
        make_trade(buy_offer)


def make_trade(buy_offer):

    while buy_offer.amount > 1:

        sell_offer = Offer.objects.filter(
            action=False,
            price__lte=buy_offer.price
        ).first()

        if not sell_offer:
            break

        amount_to_buy = buy_offer.amount
        amount_to_sell = sell_offer.amount

        if amount_to_buy > amount_to_sell:
            trade_amount_to_buy_more(buy_offer, sell_offer, amount_to_sell)

        elif amount_to_buy < amount_to_sell:
            trade_amount_to_buy_less(buy_offer, sell_offer, amount_to_buy)

        else:
            trade_amount_to_buy_equal(buy_offer, sell_offer, amount_to_buy)


def trade_amount_to_buy_more(buy_offer, sell_offer, amount):

    Trade.objects.create(
        buyer=buy_offer.user,
        seller=sell_offer.user,
        item=buy_offer.item,
        amount=amount,
        price=sell_offer.price
    )

    sell_offer.delete()

    buy_offer.amount -= amount
    buy_offer.save()


def trade_amount_to_buy_less(buy_offer, sell_offer, amount):

    Trade.objects.create(
        buyer=buy_offer.user,
        seller=sell_offer.user,
        item=buy_offer.item,
        amount=amount,
        price=sell_offer.price
    )

    buy_offer.delete()

    sell_offer.amount -= amount
    buy_offer.save()


def trade_amount_to_buy_equal(buy_offer, sell_offer, amount):

    Trade.objects.create(
        buyer=buy_offer.user,
        seller=sell_offer.user,
        item=buy_offer.item,
        amount=amount,
        price=sell_offer.price
    )

    buy_offer.delete()
    sell_offer.delete()