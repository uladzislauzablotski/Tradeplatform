from tradeplatform.celery import app
from django.core.mail import send_mail

@app.task
def send_mail_task(*args):

    send_mail(*args)

