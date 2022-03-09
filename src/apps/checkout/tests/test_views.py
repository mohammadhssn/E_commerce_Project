import pytest
from pytest_django.asserts import assertTemplateUsed, assertRedirects

from django.urls import reverse


class TestViews:

    def test_checkout_view_delivery_choices_with_invalid_user(self, db, client):
        """
            test can't access to view deliver choices
        """

        url = reverse('checkout:delivery_choices')
        response = client.get(url)
        redirect_url = f"{reverse('account:login')}?next={url}"

        assert response.status_code == 302
        assertRedirects(response, redirect_url)

    def test_checkout_view_delivery_choices_with_valid_user(self, user, client):
        """
            test access to view deliver choices valid
        """
        client.force_login(user)

        url = reverse('checkout:delivery_choices')
        response = client.get(url)

        assert response.status_code == 200
        assertTemplateUsed(response, 'checkout/delivery_choices.html')

    def test_checkout_view_basket_update_delivery_with_invalid_method_get(self, user, client):
        """
            Test can't access to view basket_update_delivery with method GET
        """

        client.force_login(user)

        url = reverse('checkout:basket_update_delivery')
        response = client.get(url)

        assert response.status_code == 405

    @pytest.mark.skip
    def test_checkout_view_basket_update_delivery_with_invalid_user_method_post(self, user, client):
        """
            Test can't access to view basket_update_delivery with method POST invalid
        """

        pass

    @pytest.mark.skip
    def test_checkout_view_basket_update_delivery_with_valid_user_method_post(self, user, client):
        """
            Test access to view basket_update_delivery with method POST Valid
        """

        pass

    def test_checkout_delivery_address_view_with_not_session_purchase_method_get(self, db, client):
        """
            Test can't access to view DeliveryAddressView with not session purchase
        """

        url = reverse('checkout:delivery_address')
        response = client.get(url)

        assert response.status_code == 302
        assertRedirects(response, reverse('catalogue:home'))

    def test_checkout_delivery_address_view_with_invalid_user_method_get(self, set_session_purchase, client):
        """
            Test can't access to view DeliveryAddressView with invalid user
        """

        url = reverse('checkout:delivery_address')
        response = client.get(url)
        redirect_url = f"{reverse('account:login')}?next={url}"

        assert response.status_code == 302
        assertRedirects(response, redirect_url)

    def test_checkout_delivery_address_view_with_valid_user_method_get(self, user, set_session_purchase, client):
        """
            Test access to view DeliveryAddressView with session purchase and valid user
        """

        client.force_login(user)
        url = reverse('checkout:delivery_address')
        response = client.get(url)

        assert response.status_code == 200
        assertTemplateUsed(response, 'checkout/delivery_address.html')

    ################################
    def test_checkout_payment_selection_view_with_not_session_address_method_get(self, db, client):
        """
            Test can't access to view PaymentSelectionView with not session address
        """

        url = reverse('checkout:payment_selection')
        response = client.get(url)

        assert response.status_code == 302
        assertRedirects(response, reverse('catalogue:home'))

    def test_checkout_payment_selection_view_with_invalid_user_method_get(self, set_session_address, client):
        """
            Test can't access to view PaymentSelectionView with session address and invalid user
        """

        url = reverse('checkout:payment_selection')
        response = client.get(url)
        redirect_url = f"{reverse('account:login')}?next={url}"

        assert response.status_code == 302
        assertRedirects(response, redirect_url)

    def test_checkout_payment_selection_view_with_valid_user_method_get(self, user, set_session_address, client):
        """
            Test access to view PaymentSelectionView with session address and valid user
        """

        client.force_login(user)
        url = reverse('checkout:payment_selection')
        response = client.get(url)

        assert response.status_code == 200
        assertTemplateUsed(response, 'checkout/payment_selection.html')
