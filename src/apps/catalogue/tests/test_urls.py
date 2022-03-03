import pytest

from django.urls import reverse, resolve

from apps.catalogue.views import HomeView, CategoryListView, ProductDetailView


class TestUrls:

    def test_home_url(self):
        """
            test home url
        """

        url = reverse('catalogue:home')

        assert resolve(url).func.view_class == HomeView

    def test_prodcut_detail_url(self):
        """
            test home url
        """

        url = reverse('catalogue:product_detail', args=['12345'])

        assert resolve(url).func.view_class == ProductDetailView

    def test_category_list_url(self):
        """
            test home url
        """

        url = reverse('catalogue:category', args=['tset_cat'])

        assert resolve(url).func.view_class == CategoryListView
