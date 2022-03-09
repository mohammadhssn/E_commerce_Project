from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from .models import DeliveryOption
from ..basket.basket import Basket
from apps.account.models import Address


class DeliveryChoicesView(LoginRequiredMixin, View):
    """
        show all delivery option if is_active=True
    """
    template_name = 'checkout/delivery_choices.html'

    def get(self, request):
        delivery_options = DeliveryOption.objects.filter(is_active=True)
        is_active_option = False
        if 'purchase' in request.session:
            is_active_option = request.session['purchase']['delivery_id']
        return render(request, self.template_name,
                      {'delivery_options': delivery_options, 'is_active_option': is_active_option})


class BasketUpdateDeliveryView(LoginRequiredMixin, View):
    """
        select delivery choices
        input: delivery_id from request POST
        get delivery_option with input(delivery_id) and update basket session with delivery_price
        and create or get session['purchase']
        output: return total price and delivery_price
    """

    def post(self, request):
        basket = Basket(request)
        delivery_option = int(request.POST.get('delivery_option'))
        delivery_type = get_object_or_404(DeliveryOption, id=delivery_option)
        update_total_price = basket.basket_update_delivery(delivery_type.delivery_price)

        session = request.session
        if 'purchase' not in request.session:
            session['purchase'] = {
                'delivery_id': delivery_type.id
            }
        else:
            session['purchase']['delivery_id'] = delivery_type.id
            session.modified = True

        response = JsonResponse({'total': update_total_price, 'delivery_price': delivery_type.delivery_price})
        return response


class DeliveryAddressView(LoginRequiredMixin, View):
    """
        Set address for delivery
        input: user must be login in site
        and session ['purchase'] exists.
        output: set address
    """

    template_name = 'checkout/delivery_address.html'

    def dispatch(self, request, *args, **kwargs):
        if 'purchase' not in request.session:
            messages.success(request, 'Please select delivery option', 'success')
            try:
                return redirect(request.META.get('HTTP_REFERER'))
            except TypeError:
                return redirect('catalogue:home')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        session = request.session
        addresses = Address.objects.filter(customer=request.user).order_by('-default')
        if addresses:
            if 'address' not in request.session:
                session['address'] = {'address_id': str(addresses[0].id)}
            else:
                session['address']['address_id'] = str(addresses[0].id)
                session.modified = True

        return render(request, self.template_name, {'addresses': addresses})


class PaymentSelectionView(LoginRequiredMixin, View):
    """
        View total prices and payment methods
        user must be logged in site
    """

    template_name = 'checkout/payment_selection.html'

    def dispatch(self, request, *args, **kwargs):
        if 'address' not in request.session:
            messages.info(request, 'Please select address option')
            try:
                return redirect(request.META.get('HTTP_REFERER'))
            except TypeError:
                return redirect('catalogue:home')

        return super().dispatch(request, *args, **kwargs)

    def get(self, request):

        return render(request, self.template_name)
