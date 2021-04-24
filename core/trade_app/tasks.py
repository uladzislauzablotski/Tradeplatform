from tradeplatform.celery import app
from trade_app.scripts import Trading


@app.task
def make_trades():
    Trading.make_trades_for_buy_offers()

