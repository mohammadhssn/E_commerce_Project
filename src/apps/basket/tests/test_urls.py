import pytest

from django.urls import reverse, resolve

from .. import views


class TestUrls:

    def test_basket_basket_summary_url(self):
        """
            test show all items from basket summary url
        """

        url = reverse('basket:basket_summary')

        assert resolve(url).func.view_class == views.BasketSummaryView

    def test_basket_add_basket_url(self):
        """
            test add item to basket url
        """

        url = reverse('basket:basket_add')

        assert resolve(url).func.view_class == views.BasketAddView

    def test_basket_delete_basket_url(self):
        """
            test delete item to basket url
        """

        url = reverse('basket:basket_delete')

        assert resolve(url).func.view_class == views.BasketDeleteView

    def test_basket_update_basket_url(self):
        """
            test update item to basket url
        """

        url = reverse('basket:basket_update')

        assert resolve(url).func.view_class == views.BasketUpdateView
