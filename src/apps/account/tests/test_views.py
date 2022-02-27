import pytest

from django.urls import reverse
from django.contrib.auth import get_user_model
from ..models import OtpCode
from ...utils import get_instance_otpcode_from_session


class TestViews:

    def test_register_view_GET(self, client):
        """
            Test register account with method GET in view
        """

        url = reverse('account:register')
        response = client.get(url)

        assert response.status_code == 200

    @pytest.mark.parametrize(
        "phone, password, password2,validity, status",
        [
            ("09192311248", "@testpass1", "@testpass1", 1, 302),
            ("09330238080", "@testpass2", "@testpass2", 1, 302),
            ("", "@testpass2", "@testpass2", 0, 200),
            ("09330238080", "", "@testpass2", 0, 200),
            ("09330238080", "testpass2", "wrongpass", 0, 200),
        ],
    )
    def test_register_view_POST(self, db, client, phone, password, password2, validity, status):
        """
            Test register account with method POST in view
        """

        url = reverse('account:register')
        data = {
            'phone': phone,
            'password': password,
            'password2': password2,
        }
        response = client.post(url, data=data)
        all_otp_code = OtpCode.objects.count()

        assert response.status_code == status
        assert all_otp_code == validity

    def test_verify_code_register_view__valid_GET(self, set_session_user_info, client):
        """
            Test view verify code with method GET with valid data
        """

        url = reverse('account:verify')
        response = client.get(url)

        # assert response.status_code == 302
        assert response.status_code == 200

    def test_verify_code_register_view__invalid_GET(self, client):
        """
            Test view verify code with method GET with invalid data
        """

        url = reverse('account:verify')
        response = client.get(url)

        assert response.status_code == 302

    def test_verify_code_register_view__valid_POST(self):
        """
            Test view verify code with method GET with valid data
        """
        pass

    def test_login_view_GET(self, client):
        """
            Test get form login with method GET
        """

        url = reverse('account:login')
        response = client.get(url)

        assert response.status_code == 200

    def test_login_view_valid_POST(self, client, user):
        """
            Test login user with method POST with valid data
        """

        url = reverse('account:login')
        response = client.post(url, data={'phone': user.phone_number, 'password': user.password})

        assert response.status_code == 302

    def test_login_view_invalid_POST(self, client, user):
        """
            Test login user with method POST with invalid data
        """

        url = reverse('account:login')
        response = client.post(url, data={'phone': '', 'password': user.password})

        assert response.status_code == 200

    def test_forget_password_view_GET(self, client):
        """
            Test forget password with method GET
        """

        url = reverse('account:forget_password')
        response = client.get(url)

        assert response.status_code == 200

    def test_forget_password_view_valid_POST(self, user, client):
        """
            Test reset password with method POST valid data
        """

        url = reverse('account:forget_password')
        data = {'phone': user.phone_number}
        response = client.post(url, data=data)

        assert response.status_code == 302

    def test_forget_password_view_invalid_POST(self, db, client):
        """
            Test reset password with method POST invalid data
        """

        url = reverse('account:forget_password')
        data = {'phone': '09122311248'}
        response = client.post(url, data=data)

        assert response.status_code == 200

    def test_reset_password_view_GET(self, set_session_reset_password, client):
        """
            Test reset password view with method GET
        """

        url = reverse('account:reset_password')
        response = client.get(url)

        assert response.status_code == 200

    def test_reset_password_view_limit_access_GET(self, client):
        """
            Test reset password done view with limit access to page
        """

        url = reverse('account:reset_password')
        response = client.get(url)

        assert response.status_code == 302

    def test_reset_password_view_POST(self, set_session_reset_password, client):
        """
            Test reset password done view with method POST
        """
        pass

    def test_reset_password_done_view_limit_access_GET(self, client):
        """
            Test limit access to page reset password done view
        """

        url = reverse('account:reset_password_done')
        response = client.get(url)

        assert response.status_code == 302

    def test_reset_password_done_view_GET(self, set_session_reset_password, client):
        """
            Test limit access to page reset password done view
        """

        url = reverse('account:reset_password_done')
        response = client.get(url)

        assert response.status_code == 200

    def test_reset_password_done_view_valid_POST(self, set_session_reset_password, client):
        """
            Test limit access to page reset password done view
        """
        pass
