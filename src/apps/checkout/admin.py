from django.contrib import admin

from .models import DeliveryOption, PaymentSelections

admin.site.register(DeliveryOption)
admin.site.register(PaymentSelections)
