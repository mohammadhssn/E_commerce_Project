import pytest

from ..forms import (
    UserCreationForm,
    UserChangeForm,

    UserRegistrationForm,
    UserLoginForm,
    VerifyCodeForm,
    ForgettingPasswordForm,
    VerifyCodePasswordForm,
    RestPasswordDoneForm,
)


class TestUserAdminPanelForm:

    @pytest.mark.parametrize(
        "phone_number, email, full_name, password1, password2, validity",
        [
            ("09192311248", "test@email.com", "", "@testpass1", "@testpass1", True),
            ("09330238080", "", "full_name", "@testpass2", "@testpass2", True),
            ("", "", "full_name", "@testpass2", "@testpass2", False),
            ("09330238080", "", "full_name", "@testpass2", "", False),
            ("09330238180", "", "full_name", "@testpass2", "wrongpass", False),
        ],
    )
    def test_user_creation_form(self, db, phone_number, email, full_name, password1, password2, validity):
        """
            Test for create a new user from admin panel
        """

        data = {
            'phone_number': phone_number,
            'email': email,
            'full_name': full_name,
            'password1': password1,
            'password2': password2,
        }

        form = UserCreationForm(data=data)

        assert form.is_valid() is validity

    @pytest.mark.parametrize(
        "phone_number, email, full_name, password,last_login, validity",
        [
            ("09192311248", "test@email.com", "", "@testpass1", "2022-02-26 18:15:24.438826", True),
            ("09330238080", "", "full_name", "@testpass2", "2022-02-26 18:15:24.438826", True),
            ("", "", "full_name", "@testpass2", "2022-02-26 18:15:24.438826", False),
            ("09330238088", "", "full_name", "", "2022-02-26 18:15:24.438826", True),
            ("09330238180", "", "full_name", "@testpass2", "2022-02-26 18:15:24.438826", True),
        ],
    )
    def test_user_change_form(self, db, phone_number, email, full_name, password, last_login, validity):
        """
            Test for change attribute user from admin panel
        """

        data = {
            'phone_number': phone_number,
            'email': email,
            'full_name': full_name,
            'password': password,
            'last_login': last_login,
        }

        form = UserChangeForm(data=data)

        assert form.is_valid() is validity


class TestUserForm:

    @pytest.mark.parametrize(
        "phone, password, password2, validity",
        [
            ("09192311248", "@testpass1", "@testpass1", True),
            ("09330238080", "@testpass2", "@testpass2", True),
            ("", "@testpass2", "@testpass2", False),
            ("09330238080", "@testpass2", "testpass2", False),
            ("09330238080", "@testpass2", "wrongpass", False),
        ],
    )
    def test_user_registration_form(self, db, phone, password, password2, validity):
        """
            Test create a new user
        """

        data = {
            'phone': phone,
            'password': password,
            'password2': password2,
        }

        form = UserRegistrationForm(data=data)

        assert form.is_valid() is validity

    @pytest.mark.parametrize(
        "code, validity",
        [
            ("123456", True),
            ("1111111111111111", False),
            ("256", True),
        ],
    )
    def test_verify_code_form(self, db, code, validity):
        """
            Test validate code
        """

        data = {
            'code': code,
        }

        form = VerifyCodeForm(data=data)

        assert form.is_valid() is validity

    def test_user_login_form(self, db):
        """
            Test login user
        """

        data = {
            'phone': '09192311248',
            'password': '09192311248A',
        }

        form = UserLoginForm(data=data)

        assert form.is_valid() is True

    def test_user_forget_password_form(self, db, user_factory):
        """
            Test forget password form
        """

        user_1 = user_factory.create(phone_number='09192311248', password='0919231248A')

        data1 = {
            'phone': user_1.phone_number
        }
        data2 = {
            'phone': '09262016512546'
        }
        data3 = {
            'phone': '123'
        }

        form1 = ForgettingPasswordForm(data=data1)
        form2 = ForgettingPasswordForm(data=data2)
        form3 = ForgettingPasswordForm(data=data3)

        assert form1.is_valid() is True
        assert form2.is_valid() is False
        assert form3.is_valid() is False

    @pytest.mark.parametrize(
        "code, validity",
        [
            ("123456", True),
            ("1111111111111111", False),
            ("256", True),
        ],
    )
    def test_verify_code_reset_password_form(self, db, code, validity):
        """
            Test validate code for reset password
        """

        data = {
            'code': code,
        }

        form = VerifyCodePasswordForm(data=data)

        assert form.is_valid() is validity

    @pytest.mark.parametrize(
        "password, password2, validity",
        [
            ("@testpass1", "@testpass1", True),
            ("", "@testpass2", False),
            ("@testpass2", "wrongpass", False),
        ],
    )
    def test_user_reset_password_done_form(self, db, password, password2, validity):
        """
            Test change password request user
        """

        data = {
            'password': password,
            'password2': password2,
        }

        form = RestPasswordDoneForm(data=data)

        assert form.is_valid() is validity
