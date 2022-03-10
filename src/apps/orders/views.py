from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.contrib import messages
from django.http import HttpResponseRedirect

from apps.orders.models import Order, OrderItem
from apps.basket.basket import Basket
from apps.account.models import Address
from apps.utils import send_email_complete_payment


class PaymentCompleteView(LoginRequiredMixin, View):
    """
        create Order & OrderItem
        input: user must be login & session basket & address must bew exists,
        output:complete order for current user
    """

    def dispatch(self, request, *args, **kwargs):
        self.user = request.user
        self.basket = Basket(request)
        try:
            self.address_session = request.session['address']['address_id']
        except KeyError:
            return redirect('catalogue:home')
        if self.user and self.basket and self.address_session:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect('catalogue:home')

    def get(self, request):
        address = get_object_or_404(Address, id=self.address_session)

        with transaction.atomic():
            order = Order.objects.create(
                user_id=self.user.id,
                full_name=self.user.full_name,
                email=self.user.email,
                phone=self.user.phone_number,
                city=address.town_city,
                address=address.address_line,
                postal_code=address.postcode,
                total_paid=self.basket.get_total_price(),
                order_key='1234',
                payment_option='payment option',
                billing_status=True
            )

            order_id = order.pk
            for item in self.basket:
                OrderItem.objects.create(
                    order_id=order_id,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['qty']
                )

            send_email_complete_payment(user=self.user)
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
