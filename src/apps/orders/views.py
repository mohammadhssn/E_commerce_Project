from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.contrib import messages

from apps.orders.models import Order, OrderItem
from apps.basket.basket import Basket
from apps.account.models import Address
from .tasks import send_email_complete_order_task


class PaymentCompleteView(LoginRequiredMixin, View):
    """
        create Order & OrderItem
        input: user must be login & session basket & address must bew exists,
        output:complete order for current user
    """

    def dispatch(self, request, *args, **kwargs):

        try:
            self.address_session = request.session['address']['address_id']
        except KeyError or self.address_session is None:
            return redirect('catalogue:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        user = request.user
        basket = Basket(request)
        address = get_object_or_404(Address, id=self.address_session)

        with transaction.atomic():
            order = Order.objects.create(
                user_id=user.id,
                full_name=user.full_name,
                email=user.email,
                phone=user.phone_number,
                city=address.town_city,
                address=address.address_line,
                postal_code=address.postcode,
                total_paid=basket.get_total_price(),
                order_key='1234',
                payment_option='payment option',
                billing_status=True
            )

            order_id = order.pk
            for item in basket:
                OrderItem.objects.create(
                    order_id=order_id,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['qty']
                )

            send_email_complete_order_task.delay(user.pk)
            messages.success(request, 'success', 'success')
            return redirect('orders:payment_success')


class PaymentSuccessfulView(LoginRequiredMixin, View):
    """
        Show message for successfully payment order
        user must be login in site
        output: clear basket session
    """

    def dispatch(self, request, *args, **kwargs):
        previous_url = request.META.get('HTTP_REFERER')
        if previous_url and 'payment-selection' in previous_url:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('catalogue:home')

    template_name = 'orders/payment_successfully.html'

    def get(self, request):
        basket = Basket(request)
        try:
            basket.clear()
        except Exception:
            pass
        return render(request, self.template_name)
