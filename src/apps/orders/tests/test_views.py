import pytest
from pytest_django.asserts import assertTemplateUsed, assertRedirects

from django.urls import reverse

from ..models import Order


class TestViews:

    def test_orders_view_order_create_with_invalid_user_and_not_session_method_get(self, db, client):
        """
            Test can't access to view CreateOrderView in method GET with invalid user and not session 'address'
        """

        url = reverse('orders:order_create')
        response = client.get(url)

        assert response.status_code == 302
        assertRedirects(response, reverse('catalogue:home'))

    def test_orders_view_order_create_with_valid_user_and_session_method_get(self, set_session_address,
                                                                             address_factory, user,
                                                                             client):
        """
            Test access to view CreateOrderView in method GET with valid user and session 'address'
        """

        client.force_login(user)
        address_factory.create(id=1, customer=user)
        # order = order_factory.create(user=user)

        url = reverse('orders:order_create')
        response = client.get(url)
        order_count = Order.objects.count()

        assert response.status_code == 302
        assert order_count == 1

    def test_orders_view_payment_successfully_with_invalid_user__method_get(self, db, client):
        """
            Test can't access to view PaymentCompleteView in method GET with invalid user
        """

        url = reverse('orders:payment_success')
        response = client.get(url)

        assert response.status_code == 302
        assertRedirects(response, reverse('catalogue:home'))

    @pytest.mark.skip
    def test_orders_view_payment_successfully_with_valid_user_method_get(self, user, client):
        """
            Test access to view PaymentCompleteView in method GET with valid user
        """
        client.force_login(user)
        url = reverse('orders:payment_success')
        response = client.get(url, HTTP_REFERER="http://127.0.0.1:8000/oreders/payment-complete/", )

        assert response.status_code == 200
        assertTemplateUsed(response, 'orders/payment_successfully.html')

    ################################

    def test_orders_payment_selection_view_with_invalid_user_method_get(self, db, client, order_factory):
        """
            Test can't access to view PaymentSelectionView with invalid user
        """

        order = order_factory.create()
        url = reverse('orders:payment_selection', args=[order.pk])
        response = client.get(url)
        redirect_url = f"{reverse('account:login')}?next={url}"

        assert response.status_code == 302
        assertRedirects(response, redirect_url)

    def test_orders_payment_selection_view_with_valid_user_method_get(self, user, client, order_factory):
        """
            Test access to view PaymentSelectionView with valid user
        """

        client.force_login(user)
        order = order_factory.create(user=user)
        url = reverse('orders:payment_selection', args=[order.pk])
        response = client.get(url)
        assert response.status_code == 200
        assertTemplateUsed(response, 'orders/payment_selection.html')

    def test_orders_apply_coupon_view_with_invalid_user_method_post(self, db, client, order_factory):
        """
            Test can't access to view ApplyCouponView with invalid user method POST
        """

        order = order_factory.create()
        url = reverse('orders:apply_coupon', args=[order.pk])
        response = client.post(url)
        redirect_url = f"{reverse('account:login')}?next={url}"

        assert response.status_code == 302
        assertRedirects(response, redirect_url)

    def test_orders_apply_coupon_view_with_valid_user_and_invalid_method_get(self, user, client, order_factory):
        """
            Test can't access to view ApplyCouponView with valid user and method Get
        """

        client.force_login(user)
        order = order_factory.create(user=user)
        url = reverse('orders:apply_coupon', args=[order.pk])
        response = client.get(url)
        assert response.status_code == 405

    def test_orders_apply_coupon_view_with_valid_user_method_post(self, user, client, order_factory):
        """
            Test can't access to view ApplyCouponView with valid user and method POST
        """

        client.force_login(user)
        order = order_factory.create(user=user)
        url = reverse('orders:apply_coupon', args=[order.pk])
        response = client.post(url)
        assert response.status_code == 302
        assertRedirects(response, reverse('orders:payment_selection', args=[order.pk]))

    def test_orders_remove_coupon_view_with_invalid_user_method_get(self, db, client, order_factory):
        """
            Test can't access to view ApplyCouponView with invalid user method GET
        """

        order = order_factory.create()
        url = reverse('orders:delete_coupon', args=[order.pk])
        response = client.get(url)
        redirect_url = f"{reverse('account:login')}?next={url}"

        assert response.status_code == 302
        assertRedirects(response, redirect_url)

    def test_orders_remove_coupon_view_with_valid_user_method_post(self, user, client, order_factory):
        """
            Test access to view ApplyCouponView with valid user and method GET
        """

        client.force_login(user)
        order = order_factory.create(user=user)
        url = reverse('orders:delete_coupon', args=[order.pk])
        response = client.get(url)
        assert response.status_code == 302
        assertRedirects(response, reverse('orders:payment_selection', args=[order.pk]))
