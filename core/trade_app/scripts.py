from rest_framework.exceptions import ValidationError


def start_rezervation(offer_data):
    """
    Reserve money if offer for buying and
    stocks if offer for selliing
    """
    action = offer_data.get('action')
    user = offer_data.get('user')
    item = offer_data.get('item')
    amount = offer_data.get('amount')
    price = offer_data.get('price')

    if action:
        reserve_for_buy_offer(user, item, amount, price)
    else:
        reserve_for_sell_offer(user, item, amount)


def get_account(user):
    'Here should be logic for choosing active account'
    return user.accounts.first()


def reserve_for_buy_offer(user, item, amount, price, **kwargs):
    """We should reserve money until the trade"""
    account = get_account(user)

    balance = account.balance
    total_buy_price = amount * price

    if balance < total_buy_price:
        raise ValidationError({
            'detail': 'You have no enough money to buy {} stocks of {}'.format(
                amount, item.code
            )
        })

    account.balance -= total_buy_price
    account.reserved_balance += total_buy_price

    account.save(update_fields=['balance', 'reserved_balance'])


def reserve_for_sell_offer(user, item, amount, **kwargs):
    """We should reserve stocks until the trade"""
    try:
        inventory = user.inventory.get(item=item)

        if inventory.amount < amount:
            raise Exception

    except Exception:
        raise ValidationError({
            'detail': 'You have no {} stocks of {} to sell.'.format(
                amount, item.code)
        })

    inventory.amount -= amount
    inventory.reserved_amount += amount

    inventory.save(update_fields=['amount', 'reserved_amount'])