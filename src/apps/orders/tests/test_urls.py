import pytest

from django.urls import reverse, resolve

from .. import views


class TestUrls:

    def test_orders_order_create_url(self):
        """
            Test access url to view CreateOrderView
        """

        url = reverse('orders:order_create')

        assert resolve(url).func.view_class == views.CreateOrderView

    def test_orders_payment_successfully_url(self):
        """
            Test access url to view PaymentSuccessfulView
        """

        url = reverse('orders:payment_success')

        assert resolve(url).func.view_class == views.PaymentSuccessfulView

    def test_orders_payment_selection_url(self):
        """
            Test access url to view PaymentSelectionView
        """

        url = reverse('orders:payment_selection', args=[1])

        assert resolve(url).func.view_class == views.PaymentSelectionView

    def test_orders_apply_coupon_url(self):
        """
            Test access url to view ApplyCouponView
        """

        url = reverse('orders:apply_coupon', args=[1])

        assert resolve(url).func.view_class == views.ApplyCouponView

    def test_orders_remove_coupon_url(self):
        """
            Test access url to view DeleteCouponView
        """

        url = reverse('orders:delete_coupon', args=[1])

        assert resolve(url).func.view_class == views.RemoveCouponView
