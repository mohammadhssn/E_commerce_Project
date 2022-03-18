import datetime

from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.contrib import messages
from apps.orders.models import Order, OrderItem, Coupon
from apps.basket.basket import Basket
from apps.account.models import Address
from .tasks import send_email_complete_order_task
from .forms import CouponForm


class CreateOrderView(LoginRequiredMixin, View):
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
                billing_status=False
            )

            order_id = order.pk
            for item in basket:
                OrderItem.objects.create(
                    order_id=order_id,
                    product=item['product'],
                    price=item['price'],
                    quantity=item['qty']
                )

            return redirect('orders:payment_selection', order.pk)


class PaymentSelectionView(LoginRequiredMixin, View):
    """
        View total prices and payment methods
        user must be logged in site
    """

    template_name = 'orders/payment_selection.html'
    form_class = CouponForm

    def get(self, request, order_id):
        basket = Basket(request)
        sub_total = basket.get_subtotal_price()
        form = self.form_class()
        order = get_object_or_404(Order, pk=order_id, user=request.user)
        if order.discount:
            discount_price = (order.discount / 100) * sub_total
            total_paid = int(sub_total - discount_price) + basket.get_delivery_price()
            order.total_paid = total_paid
            order.save(update_fields=['total_paid'])
        else:
            total_paid = basket.get_total_price()
        return render(request, self.template_name, {'order': order, 'form': form, 'total_paid': total_paid})


# class PaymentCompleteView(LoginRequiredMixin, View):
#     """
#         create Order & OrderItem
#         input: user must be login & session basket & address must bew exists,
#         output:complete order for current user
#     """
#
#     def dispatch(self, request, *args, **kwargs):
#
#         try:
#             self.address_session = request.session['address']['address_id']
#         except KeyError or self.address_session is None:
#             return redirect('catalogue:home')
#         return super().dispatch(request, *args, **kwargs)
#
#     def get(self, request):
#         user = request.user
#         basket = Basket(request)
#         address = get_object_or_404(Address, id=self.address_session)
#
#         with transaction.atomic():
#             order = Order.objects.create(
#                 user_id=user.id,
#                 full_name=user.full_name,
#                 email=user.email,
#                 phone=user.phone_number,
#                 city=address.town_city,
#                 address=address.address_line,
#                 postal_code=address.postcode,
#                 total_paid=basket.get_total_price(),
#                 order_key='1234',
#                 payment_option='payment option',
#                 billing_status=True
#             )
#
#             order_id = order.pk
#             for item in basket:
#                 OrderItem.objects.create(
#                     order_id=order_id,
#                     product=item['product'],
#                     price=item['price'],
#                     quantity=item['qty']
#                 )
#
#             send_email_complete_order_task.delay(user.pk)
#             messages.success(request, 'success', 'success')
#             return redirect('orders:payment_success')


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


class ApplyCouponView(LoginRequiredMixin, View):
    form_class = CouponForm

    def post(self, request, order_id=None):
        now = datetime.datetime.now()
        form = self.form_class(request.POST)
        if form.is_valid():
            code = form.cleaned_data['code']
            try:
                coupon = Coupon.objects.get(code__exact=code, valid_from__lte=now, valid_to__gte=now, active=True)
            except Coupon.DoesNotExist:
                messages.error(request, 'this coupon does not exists', 'danger')
                return redirect('orders:payment_selection', order_id)
            order = Order.objects.get(id=order_id, user=request.user, billing_status=False)
            order.discount = coupon.discount
            order.save()
            messages.success(request, 'Coupon Activate successful', 'success')
        return redirect('orders:payment_selection', order_id)


class RemoveCouponView(LoginRequiredMixin, View):

    def get(self, request, order_id=None):
        basket = Basket(request)
        order = get_object_or_404(Order, pk=order_id)
        if order.discount:
            order.discount = None
            order.total_paid = basket.get_total_price()
            order.save(update_fields=['discount', 'total_paid'])
            messages.warning(request, 'coupon deleted successful', 'info')
        return redirect('orders:payment_selection', order_id)
