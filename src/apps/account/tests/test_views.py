import pytest

from django.urls import reverse

from pytest_django.asserts import assertTemplateUsed, assertRedirects

from ..models import OtpCode, Address


class TestViews:

    def test_account_register_view_method_get(self, db, client):
        """
            Test register account with method GET in view
        """

        url = reverse('account:register')
        response = client.get(url)

        assert response.status_code == 200
        assertTemplateUsed(response, 'account/registration/register.html')

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
    def test_account_register_view_method_post(self, db, client, phone, password, password2, validity, status):
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

    def test_account_verify_code_register_view_valid_method_get(self, set_session_user_info, client):
        """
            Test view verify code with method GET with valid data
        """

        url = reverse('account:verify')
        response = client.get(url)

        assert response.status_code == 200
        assertTemplateUsed(response, 'account/registration/verify.html')

    def test_account_verify_code_register_view_invalid_method_get(self, db, client):
        """
            Test view verify code with method GET with invalid data
        """

        url = reverse('account:verify')
        response = client.get(url)

        assert response.status_code == 302
        assertRedirects(response, reverse('catalogue:home'))

    @pytest.mark.skip
    def test_account_verify_code_register_view__valid_method_post(self):
        """
            Test view verify code with method GET with valid data
        """
        pass

    def test_account_login_view_method_get(self, db, client):
        """
            Test get form login with method GET
        """

        url = reverse('account:login')
        response = client.get(url)

        assert response.status_code == 200
        assertTemplateUsed(response, 'account/registration/login.html')

    def test_account_login_view_valid_method_post(self, db, client, user_factory):
        """
            Test login user with method POST with valid data
        """

        user_factory.create(phone_number='09192311248', password='09192311248Pass')

        url = reverse('account:login')
        response = client.post(url, data={'phone': '09192311248', 'password': '09192311248Pass'})

        assert response.status_code == 302
        assertRedirects(response, reverse('catalogue:home'))

    def test_account_login_view_invalid_method_post(self, client, user):
        """
            Test login user with method POST with invalid data
        """

        url = reverse('account:login')
        response = client.post(url, data={'phone': '', 'password': user.password})

        assert response.status_code == 200
        assertTemplateUsed(response, 'account/registration/login.html')

    def test_account_forget_password_view__method_get(self, db, client):
        """
            Test forget password with method GET
        """

        url = reverse('account:forget_password')
        response = client.get(url)

        assert response.status_code == 200
        assertTemplateUsed(response, 'account/password/forget_password.html')

    def test_account_forget_password_view_valid_method_post(self, user, client):
        """
            Test reset password with method POST valid data
        """

        url = reverse('account:forget_password')
        data = {'phone': user.phone_number}
        response = client.post(url, data=data)

        assert response.status_code == 302
        assertRedirects(response, reverse('account:reset_password'))

    def test_account_forget_password_view_invalid_method_post(self, db, client):
        """
            Test reset password with method POST invalid data
        """

        url = reverse('account:forget_password')
        data = {'phone': '09122311248'}
        response = client.post(url, data=data)

        assert response.status_code == 200

    def test_account_reset_password_view_method_get(self, set_session_reset_password, client):
        """
            Test reset password view with method GET
        """

        url = reverse('account:reset_password')
        response = client.get(url)

        assert response.status_code == 200
        assertTemplateUsed(response, 'account/password/reset_password.html')

    def test_account_reset_password_view_limit_access_method_get(self, db, client):
        """
            Test reset password done view with limit access to page
        """

        url = reverse('account:reset_password')
        response = client.get(url)

        assert response.status_code == 302
        assertRedirects(response, reverse('catalogue:home'))

    @pytest.mark.skip
    def test_account_reset_password_view_method_post(self, set_session_reset_password, client):
        """
            Test reset password done view with method POST
        """
        pass

    def test_account_reset_password_done_view_limit_access_method_get(self, db, client):
        """
            Test limit access to page reset password done view
        """

        url = reverse('account:reset_password_done')
        response = client.get(url)

        assert response.status_code == 302
        assertRedirects(response, reverse('catalogue:home'))

    def test_account_reset_password_done_view_method_get(self, set_session_reset_password, client):
        """
            Test limit access to page reset password done view
        """

        url = reverse('account:reset_password_done')
        response = client.get(url)

        assert response.status_code == 200
        assertTemplateUsed(response, 'account/password/reset_password_done.html')

    @pytest.mark.skip
    def test_account_reset_password_done_view_valid_method_post(self, set_session_reset_password, client):
        """
            Test limit access to page reset password done view
        """
        pass

    def test_account_dashboard_view_valid_user_method_get(self, db, client, user):
        """
            Test dashboard current user & user must be login to site
        """

        url = reverse('account:dashboard')
        client.force_login(user)
        response = client.get(url)

        assert response.status_code == 200
        assertTemplateUsed(response, 'account/dashboard/dashboard.html')

    def test_account_dashboard_view_invalid_user_method_get(self, db, client):
        """
            Test dashboard with not user
        """

        url = reverse('account:dashboard')
        response = client.get(url)
        redirect_url = f"{reverse('account:login')}?next={url}"

        assert response.status_code == 302
        assertRedirects(response, redirect_url)

    def test_account_edit_profile_valid_user_method_get(self, db, client, user):
        """
            Test edit profile current user & user must be login to site
        """

        url = reverse('account:edit_profile')
        client.force_login(user)
        response = client.get(url)

        assert response.status_code == 200
        assertTemplateUsed(response, 'account/dashboard/edit_profile.html')

    def test_account_edit_profile_invalid_user_method_get(self, db, client):
        """
            Test edit profile with not user
        """

        url = reverse('account:edit_profile')
        response = client.get(url)
        redirect_url = f"{reverse('account:login')}?next={url}"

        assert response.status_code == 302
        assertRedirects(response, redirect_url)

    def test_account_edit_profile_valid_user_method_post(self, db, client, user):
        """
            Test edit profile current user with method POST & user must be login to site
        """

        url = reverse('account:edit_profile')
        client.force_login(user)
        data = {
            'phone_number': user.phone_number,
            'full_name': 'mohammadhssn',
            'email': 'mohammadhssn@email.com'
        }
        response = client.post(url, data=data)

        assert response.status_code == 302
        assertRedirects(response, reverse('account:dashboard'))

    def test_account_edit_profile_invalid_user_method_post(self, db, client):
        """
            Test edit profile current user with method POST & user must be login to site
        """

        url = reverse('account:edit_profile')
        data = {
            'phone_number': '',
            'full_name': 'mohammadhssn',
            'email': 'mohammadhssn@email.com'
        }
        response = client.post(url, data=data)
        redirect_url = f"{reverse('account:login')}?next={url}"

        assert response.status_code == 302
        assertRedirects(response, redirect_url)


class TestViewAddress:

    def test_account_home_address_view_with_invalid_user_method_get(self, db, client):
        """
            Test can't access to address home with invalid user
        """

        url = reverse('account:addresses')
        response = client.get(url)
        redirect_url = f"{reverse('account:login')}?next={url}"

        assert response.status_code == 302
        assertRedirects(response, redirect_url)

    def test_account_home_address_view_with_valid_user_method_get(self, user, client):
        """
            Test can't access to address home with invalid user
        """

        client.force_login(user)
        url = reverse('account:addresses')
        response = client.get(url)

        assert response.status_code == 200
        assertTemplateUsed(response, 'account/dashboard/addresses.html')

    def test_account_add_address_view_with_invalid_user_method_get(self, db, client):
        """
            Test can't access to add address view with invalid user
        """

        url = reverse('account:add_addresses')
        response = client.get(url)
        redirect_url = f"{reverse('account:login')}?next={url}"

        assert response.status_code == 302
        assertRedirects(response, redirect_url)

    def test_account_add_address_view_with_valid_user_method_get(self, user, client):
        """
            Test access to add address view with valid user
        """

        client.force_login(user)
        url = reverse('account:add_addresses')
        response = client.get(url)

        assert response.status_code == 200
        assertTemplateUsed(response, 'account/dashboard/add_edit_addresses.html')

    def test_account_add_address_view_with_invalid_user_method_post(self, db, client):
        """
            Test can't access to add address view with invalid user in method POST
        """

        url = reverse('account:add_addresses')
        data = {
            'full_name': 'kevin A',
            'phone': '09192311248',
            'address_line': 'iran',
            'address_line2': 'iran2',
            'town_city': 'tehran',
            'postcode': '12345'
        }
        response = client.post(url, data=data)
        all_address = Address.objects.count()
        redirect_url = f"{reverse('account:login')}?next={url}"

        assert response.status_code == 302
        assert all_address == 0
        assertRedirects(response, redirect_url)

    def test_account_add_address_view_with_valid_user_method_post(self, user, client):
        """
            Test access to add address view with valid user in method POST
        """

        client.force_login(user)
        url = reverse('account:add_addresses')
        data = {
            'full_name': 'kevin A',
            'phone': '09192311248',
            'address_line': 'iran',
            'address_line2': 'iran2',
            'town_city': 'tehran',
            'postcode': '12345'
        }
        response = client.post(url, data=data)
        all_address = Address.objects.count()

        assert response.status_code == 302
        assert all_address == 1
        assertRedirects(response, reverse('account:addresses'))

    def test_account_edit_address_view_with_valid_user_method_get(self, user, client, address_factory):
        """
            Test access to edit address view with valid user
        """

        client.force_login(user)

        address = address_factory.create(customer=user)
        url = reverse('account:edit_addresses', args=[address.id])
        response = client.get(url)

        assert response.status_code == 200
        assertTemplateUsed(response, 'account/dashboard/add_edit_addresses.html')

    def test_account_edit_address_view_with_invalid_user_method_get(self, db, user, client, address_factory):
        """
            Test can't access to edit address view with valid user
        """

        address = address_factory.create(customer=user)
        url = reverse('account:edit_addresses', args=[address.id])
        with pytest.raises(TypeError) as error:
            client.get(url)

        assert str(error.value) == "'AnonymousUser' object is not iterable"

    def test_account_edit_address_view_with_valid_user_method_post(self, user, address_factory, client):
        """
            Test access to edit address view with valid user in method POST
        """

        client.force_login(user)

        address = address_factory.create(customer=user)

        url = reverse('account:edit_addresses', args=[address.id])
        data = {
            'full_name': 'kevin A',
            'phone': '09192311248',
            'address_line': 'iran',
            'address_line2': 'iran2',
            'town_city': 'tehran',
            'postcode': '12345'
        }
        response = client.post(url, data=data)
        all_address = Address.objects.count()

        assert response.status_code == 302
        assert all_address == 1
        assertRedirects(response, reverse('account:addresses'))

    def test_account_delete_address_view_with_invalid_user_method_get(self, user, address_factory, client):
        """
            Test can't access to delete address view with invalid user in method GET
        """

        address = address_factory.create(customer=user)
        url = reverse('account:delete_addresses', args=[address.id])
        response = client.get(url)
        all_address = Address.objects.count()
        redirect_url = f"{reverse('account:login')}?next={url}"

        assert response.status_code == 302
        assert all_address == 1
        assertRedirects(response, redirect_url)

    def test_account_delete_address_view_with_valid_user_method_get(self, user, address_factory, client):
        """
            Test access to delete address view with valid user in method GET
        """

        client.force_login(user)

        address = address_factory.create(customer=user)
        url = reverse('account:delete_addresses', args=[address.id])
        response = client.get(url)
        all_address = Address.objects.count()

        assert response.status_code == 302
        assert all_address == 0
        assertRedirects(response, reverse('account:addresses'))

    def test_account_set_default_address_view_with_invalid_user_method_get(self, user, address_factory,
                                                                           client):
        """
            Test can't access to set default address view with invalid user in method GET
        """

        address = address_factory.create(customer=user)
        url = reverse('account:set_default_addresses', args=[address.id])
        response = client.get(url)
        redirect_url = f"{reverse('account:login')}?next={url}"

        assert response.status_code == 302
        assertRedirects(response, redirect_url)

    def test_account_set_default_address_view_with_valid_user_method_get(self, user, address_factory,
                                                                         client):
        """
            Test access to set default address view with valid user in method GET
        """

        client.force_login(user)
        address = address_factory.create(customer=user, default=False)
        url = reverse('account:set_default_addresses', args=[address.id])
        response = client.get(url)
        response_address = Address.objects.get(id=address.id)

        assert response.status_code == 302
        assert response_address.default is True
        assertRedirects(response, reverse('account:addresses'))
