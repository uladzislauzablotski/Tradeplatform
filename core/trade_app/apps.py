from django.apps import AppConfig


class TradeAppConfig(AppConfig):
    name = 'trade_app'

    def ready(self):
        import trade_app.receivers
