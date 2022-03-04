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
