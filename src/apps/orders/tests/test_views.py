import pytest
from pytest_django.asserts import assertTemplateUsed, assertRedirects

from django.urls import reverse

from apps.account.models import Address


class TestViews:

    def test_orders_view_payment_complete_with_invalid_user_and_not_session_method_get(self, db, client):
        """
            Test can't access to view PaymentCompleteView in method GET with invalid user and not session 'address'
        """

        url = reverse('orders:payment_complete')
        response = client.get(url)

        assert response.status_code == 302
        assertRedirects(response, reverse('catalogue:home'))

    def test_orders_view_payment_complete_with_valid_user_and_session_method_get(self, set_session_address,
                                                                                 address_factory, user,
                                                                                 client):
        """
            Test access to view PaymentCompleteView in method GET with valid user and session 'address'
        """

        client.force_login(user)
        address_factory.create(id=1, customer=user)

        url = reverse('orders:payment_complete')
        response = client.get(url)

        assert response.status_code == 302

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
