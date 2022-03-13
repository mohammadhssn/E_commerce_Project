from celery import shared_task

from apps.utils import send_email_complete_payment


@shared_task
def send_email_complete_order_task(pk=None):
    return send_email_complete_payment(pk)
