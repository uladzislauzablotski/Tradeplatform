from rest_framework.exceptions import ValidationError
from trade_app.models import Inventory, Offer, Trade
from django.db import transaction
from django.shortcuts import get_object_or_404


def get_account(user):
    'Here should be logic for choosing active account'
    return user.accounts.first()


class Reservation():

    @classmethod
    def start_reservation(cls, offer_data):

        action = offer_data.get('action')
        user = offer_data.get('user')
        item = offer_data.get('item')
        amount = offer_data.get('amount')
        price = offer_data.get('price')

        if action:
            return cls._reserve_for_buy_offer(
                user,
                item,
                amount,
                price
            )
        else:
            return cls._reserve_for_sell_offer(
                user,
                item,
                amount
            )

    @staticmethod
    def _reserve_for_buy_offer(user, item, amount, price):
        """We should reserve money until the trade"""
        account = get_account(user)

        balance = account.balance
        total_buy_price = amount * price

        if balance < total_buy_price:
            raise ValidationError({
                'detail': f'You have no enough money to buy {amount} stocks of {item.code}'
            })

        account.balance -= total_buy_price
        account.reserved_balance += total_buy_price

        return account.save(update_fields=['balance', 'reserved_balance'])

    @staticmethod
    def _reserve_for_sell_offer(user, item, amount):
        """We should reserve stocks until the trade"""
        try:
            inventory = user.inventory.get(item=item)

            if inventory.amount < amount:
                raise ValidationError

        except Inventory.DoesNotExist or ValidationError:
            raise ValidationError({
                'detail': f'You have no {amount} stocks of {item.code} to sell.'
            })

        inventory.amount -= amount
        inventory.reserved_amount += amount

        return inventory.save(update_fields=['amount', 'reserved_amount'])


class Trading():

    @classmethod
    def make_trades_for_buy_offers(cls):
        buy_offers = Offer.objects.filter(action=True).order_by('created_at')

        for buy_offer in buy_offers:

            while True:

                next = cls._find_suitable_sell_offer_and_make_trade(buy_offer)

                if not next:
                    "There is no suitable offer" \
                        "or there is no more need in to find offers for buyer"
                    break

    @classmethod
    @transaction.atomic
    def _find_suitable_sell_offer_and_make_trade(cls, buy_offer):
        sell_offer = cls._find_sell_offer_suitable_for_buy_price(buy_offer.price)

        if not sell_offer:
            "If there is no suitable offer"
            return None

        return cls._make_trade(buy_offer, sell_offer)

    @classmethod
    def _make_trade(cls, buy_offer, sell_offer):
        amount_to_buy = buy_offer.amount
        amount_to_sell = sell_offer.amount

        if amount_to_buy > amount_to_sell:
            return cls._trade_amount_to_buy_more(buy_offer, sell_offer, amount_to_sell)

        elif amount_to_buy < amount_to_sell:
            return cls._trade_amount_to_buy_less(buy_offer, sell_offer, amount_to_buy)

        elif amount_to_buy == amount_to_sell:
            return cls._trade_amount_to_buy_equal(buy_offer, sell_offer, amount_to_buy)

    @classmethod
    def _trade_amount_to_buy_more(cls, buy_offer, sell_offer, amount):
        buy_offer.amount += amount
        buy_offer.save(update_fields=['amount'])

        cls._change_inventory_balance_and_make_trade(buy_offer, sell_offer, amount)

        sell_offer.delete()

        return True

    @classmethod
    def _trade_amount_to_buy_less(cls, buy_offer, sell_offer, amount):
        sell_offer.amount -= amount
        sell_offer.save(update_fields=['amount'])

        cls._change_inventory_balance_and_make_trade(buy_offer, sell_offer, amount)

        buy_offer.delete()

        """There is no more need to find offers for this buy-offer"""
        return False

    @classmethod
    def _trade_amount_to_buy_equal(cls, buy_offer, sell_offer, amount):
        cls._change_inventory_balance_and_make_trade(buy_offer, sell_offer, amount)

        sell_offer.delete()
        buy_offer.delete()

        """There is no more need to find offers for this buy-offer"""
        return False

    @classmethod
    def _change_inventory_balance_and_make_trade(cls, buy_offer, sell_offer, amount):

        price = sell_offer.price

        cls._change_buyer_inventory(buy_offer, amount)
        cls._change_seller_inventory(sell_offer, amount)
        cls._change_buyer_balance(buy_offer, price, amount)
        cls._change_seller_balance(sell_offer, price, amount)

        cls._create_trade(buy_offer, sell_offer, amount)

    @staticmethod
    def _change_buyer_inventory(buy_offer, amount):
        user = buy_offer.user
        item = buy_offer.item

        inventory, created = Inventory.objects.filter(item=item).get_or_create(
            user=user,
            defaults={
                'item': item
            }
        )

        inventory.amount += amount

        inventory.save(update_fields=['amount'])

    @staticmethod
    def _change_seller_inventory(sell_offer, amount):
        user = sell_offer.user
        item = sell_offer.item

        inventory = get_object_or_404(Inventory.objects.filter(item=item), user=user)

        inventory.reserved_amount -= amount

        inventory.save(update_fields=['reserved_amount'])

    @staticmethod
    def _change_buyer_balance(buy_offer, price, amount):
        user = buy_offer.user

        account = get_account(user)

        agreed_price = buy_offer.price  # user agreed for this price
        actual_price = price  # this is price of seller, which can be less than agreed price

        '''Buyer saved money because of delta of agreed price and actual price'''
        saved = (agreed_price - actual_price) * amount

        account.balance += saved
        account.reserved_balance -= amount * agreed_price

        account.save(update_fields=['balance', 'reserved_balance'])

    @staticmethod
    def _change_seller_balance(sell_offer, price, amount):
        user = sell_offer.user

        account = get_account(user)
        account.balance += (amount * price)

        account.save(update_fields=['balance'])

    @staticmethod
    def _find_sell_offer_suitable_for_buy_price(price):
        return Offer.objects.filter(
            action=False,
            price__lte=price
        ).first()

    @staticmethod
    def _create_trade(buy_offer, sell_offer, amount):
        return Trade.objects.create(
            buyer=buy_offer.user,
            seller=sell_offer.user,
            item=buy_offer.item,
            amount=amount,
            price=sell_offer.price
        )
