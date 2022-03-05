from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import DeliveryOption
from ..basket.basket import Basket


class DeliveryChoices(LoginRequiredMixin, View):
    """
        show all delivery option if is_active=True
    """
    template_name = 'checkout/delivery_choices.html'

    def get(self, request):
        delivery_options = DeliveryOption.objects.filter(is_active=True)
        return render(request, self.template_name, {'delivery_options': delivery_options})


class BasketUpdateDelivery(LoginRequiredMixin, View):
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
