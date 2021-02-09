from celery import Celery

app = Celery("worker")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'make_trades': {
        'task': 'trade_app.tasks.make_trades',
        'schedule': 60.0,
    },
}