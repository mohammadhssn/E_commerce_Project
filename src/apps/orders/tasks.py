import datetime

from django.utils import timezone

from celery import shared_task

from apps.utils import send_email_complete_payment
from apps.orders.models import Order


@shared_task
def send_email_complete_order_task(pk=None):
    return send_email_complete_payment(pk)


# @shared_task
# def delete_expired_orders_task():
#     one_days = datetime.datetime.now() - timezone.timedelta(days=1)
#     orders = Order.objects.filter(billing_status=False, created__gt=one_days)
#     orders.delete()
#     print('run tasks...')
#     return True
