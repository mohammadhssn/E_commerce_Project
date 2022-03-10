from django.shortcuts import render, get_object_or_404
from django.views import View
from django.http import JsonResponse

from .basket import Basket

from apps.catalogue.models import ProductInventory


class BasketSummaryView(View):
    """
        show all items in session basket in view
    """
    template_name = 'basket/basket_summary.html'

    def get(self, request):
        basket = Basket(request)

        return render(request, self.template_name, {'basket': basket})


class BasketAddView(View):
    """
        Add product in basket session
        input: product_id & product_qty from request POST
        and get product and send to basket method basket.add()
        output: sum quantity products
    """

    def post(self, request):
        basket = Basket(request)
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        product = get_object_or_404(ProductInventory, id=product_id)
        basket.add(product=product, qty=product_qty)
        basket_qty = basket.__len__()
        response = JsonResponse({'qty': basket_qty})
        return response


class BasketDeleteView(View):
    """
        Delete item form basket
        input: product_id from request POST
        and delete item form basket with method basket.delete()
        output: sum quantity products and total price items

    """

    def post(self, request):
        basket = Basket(request)
        product_id = int(request.POST.get('product_id'))
        basket.delete(product=product_id)

        basket_qty = basket.__len__()
        basket_total = basket.get_total_price()
        response = JsonResponse({'qty': basket_qty, 'subtotal': basket_total})
        return response


class BasketUpdateView(View):
    """
        update item form basket
        input: product_id & product_qty from request POST
        and update item form basket with method basket.update()
        output: sum quantity items and total price items

    """

    def post(self, request):
        basket = Basket(request)
        product_id = int(request.POST.get('product_id'))
        product_qty = int(request.POST.get('product_qty'))
        basket.update(product=product_id, qty=product_qty)

        basket_qty = basket.__len__()
        basket_total = basket.get_total_price()
        response = JsonResponse({'qty': basket_qty, 'subtotal': basket_total})
        return response
