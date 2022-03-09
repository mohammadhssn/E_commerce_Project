import uuid

import pytest

from django.urls import reverse, resolve

from .. import views


class TestUrls:

    def test_account_register_url(self):
        """
            test register url
        """

        url = reverse('account:register')

        assert resolve(url).func.view_class == views.RegisterView

    def test_account_register_verify_code_url(self):
        """
            test register verify url
        """

        url = reverse('account:verify')

        assert resolve(url).func.view_class == views.UserRegisterVerifyCodeView

    def test_account_login_url(self):
        """
            test login user  url
        """

        url = reverse('account:login')

        assert resolve(url).func.view_class == views.UserLoginView

    def test_account_forget_password_url(self):
        """
            test forget passwrd url
        """

        url = reverse('account:forget_password')

        assert resolve(url).func.view_class == views.ForgettingPasswordView

    def test_account_reset_password_url(self):
        """
            test reset passwrd url
        """

        url = reverse('account:reset_password')

        assert resolve(url).func.view_class == views.ResetPasswordView

    def test_account_reset_password_done_url(self):
        """
            test reset passwrd done url
        """

        url = reverse('account:reset_password_done')

        assert resolve(url).func.view_class == views.ResetPasswordDoneView

    def test_account_dashboard_url(self):
        """
            test account dashboard url
        """

        url = reverse('account:dashboard')

        assert resolve(url).func.view_class == views.DashboardView

    def test_account_edit_profile_url(self):
        """
            test account edit profile url
        """

        url = reverse('account:edit_profile')

        assert resolve(url).func.view_class == views.EditProfileView

    # address
    def test_account_addresses_url(self):
        """
            Test address url can connect to view AddressView
        """

        url = reverse('account:addresses')

        assert resolve(url).func.view_class == views.AddressView

    def test_account_add_addresses_url(self):
        """
            Test add address url can connect to view AddAddressView
        """

        url = reverse('account:add_addresses')

        assert resolve(url).func.view_class == views.AddAddressView

    def test_account_edit_addresses_url(self):
        """
            Test edit address url can connect to view EditAddressView
        """

        uuid_id = uuid.uuid4()
        url = reverse('account:edit_addresses', args=[uuid_id])

        assert resolve(url).func.view_class == views.EditAddressView

    def test_account_delete_addresses_url(self):
        """
            Test delete address url can connect to view DeleteAddressView
        """

        uuid_id = uuid.uuid4()
        url = reverse('account:delete_addresses', args=[uuid_id])

        assert resolve(url).func.view_class == views.DeleteAddressView

    def test_account_set_default_addresses_url(self):
        """
            Test set default address url can connect to view SetDefaultAddressView
        """

        uuid_id = uuid.uuid4()
        url = reverse('account:set_default_addresses', args=[uuid_id])

        assert resolve(url).func.view_class == views.SetDefaultAddressView

    def test_account_wash_list_url(self):
        """
            Test wash list url can connect to view WashListView
        """
        url = reverse('account:wash_list')

        assert resolve(url).func.view_class == views.WashListView

    def test_account_add_wash_list_url(self):
        """
            Test wash list url can connect to view AddWashListView
        """

        url = reverse('account:add_wash_list', args=[1])

        assert resolve(url).func.view_class == views.AddWashListView
