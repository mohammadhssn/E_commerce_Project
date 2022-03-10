from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.contrib import messages

from apps.orders.models import Order, OrderItem
from apps.basket.basket import Basket
from apps.account.models import Address


class PaymentCompleteView(LoginRequiredMixin, View):

    def get(self, request):
        user = request.user
        basket = Basket(request)
        address_session = request.session['address']['address_id']
        address = get_object_or_404(Address, id=address_session)

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

        messages.success(request, 'success', 'success')
        return redirect('orders:payment_success')


class PaymentSuccessfulView(LoginRequiredMixin, View):
    template_name = 'orders/payment_successfully.html'

    def get(self, request):
        basket = Basket(request)
        try:
            basket.clear()
        except Exception:
            pass
        return render(request, self.template_name)
