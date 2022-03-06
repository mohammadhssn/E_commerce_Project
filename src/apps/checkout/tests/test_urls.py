import pytest

from django.urls import reverse, resolve

from .. import views


class TestUrls:

    def test_checkout_delivery_option_url(self):
        """
            Test access url in view DeliveryChoices
        """

        url = reverse('checkout:delivery_choices')

        assert resolve(url).func.view_class == views.DeliveryChoicesView

    def test_checkout_basket_update_url(self):
        """
            Test access url in view BasketUpdateDeliveryView
        """

        url = reverse('checkout:basket_update_delivery')

        assert resolve(url).func.view_class == views.BasketUpdateDeliveryView
