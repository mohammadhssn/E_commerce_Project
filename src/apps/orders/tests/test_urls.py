import pytest

from django.urls import reverse, resolve

from .. import views


class TestUrls:

    def test_orders_payment_complete_url(self):
        """
            Test access url to view PaymentCompleteView
        """

        url = reverse('orders:payment_complete')

        assert resolve(url).func.view_class == views.PaymentCompleteView

    def test_orders_payment_successfully_url(self):
        """
            Test access url to view PaymentSuccessfulView
        """

        url = reverse('orders:payment_success')

        assert resolve(url).func.view_class == views.PaymentSuccessfulView
