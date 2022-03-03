import pytest
from pytest_django.asserts import assertTemplateUsed

from django.urls import reverse


class TestViews:

    def test_catalogue_view_home(self, db, client):
        """
            Test access to home view
        """

        url = reverse('catalogue:home')
        response = client.get(url)

        assert response.status_code == 200
        assertTemplateUsed(response, 'catalogue/home.html')

    def test_catalogue_view_product_detail(self, db, client, product_inventory_factory):
        """
            Test access to product detail view with product_web_id
        """
        product = product_inventory_factory.create(product__web_id='123456789', is_default=True)

        url = reverse('catalogue:product_detail', args=[product.product.web_id])
        response = client.get(url)

        assert response.status_code == 200
        assertTemplateUsed(response, 'catalogue/product_detail.html')

    def test_catalogue_view_category_list(self, db, client, category_factory):
        """
            Test access to category list view valid category
        """

        category_1 = category_factory.create(name='cat_1', slug='cat-1')
        url = reverse('catalogue:category', args=[category_1.slug])
        response = client.get(url)

        assert response.status_code == 200
        assertTemplateUsed(response, 'catalogue/category.html')
        assert response.context['page_obj'].number == response.context['page_obj'].paginator.page(1).number
