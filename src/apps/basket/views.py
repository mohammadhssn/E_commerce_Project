from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import JsonResponse

from .basket import Basket

from apps.catalogue.models import ProductInventory


class BasketSummaryView(View):
    """
        Show basket summary
    """

    def get(self, request):
        basket = Basket(request)

        return render(request, 'basket/basket_summary.html', {'basket': basket})


class BasketAddView(View):
    """
        Add product in basket
    """

    def post(self, request):
        basket = Basket(request)
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        product = get_object_or_404(ProductInventory, id=product_id)
        basket.add(product=product, qty=product_qty)
        basketqty = basket.__len__()
        response = JsonResponse({'qty': basketqty})
        return response


class BasketDeleteView(View):
    """
        Delete item form basket
    """

    def post(self, request):
        basket = Basket(request)
        product_id = int(request.POST.get('productid'))
        basket.delete(product=product_id)

        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
        return response


class BasketUpdateView(View):
    """
        Delete item form basket
    """

    def post(self, request):
        basket = Basket(request)
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        basket.update(product=product_id, qty=product_qty)

        basketqty = basket.__len__()
        baskettotal = basket.get_total_price()
        response = JsonResponse({'qty': basketqty, 'subtotal': baskettotal})
        return response
