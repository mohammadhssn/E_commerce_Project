import random

import pytest

from django.contrib.auth import get_user_model

from apps.account.models import Address


class TestUserModel:
    """
        Test model User
    """

    def test_account_user_str(self, user):
        """
            Test the user string representation
        """

        assert user.is_active is False
        assert user.__str__() == '09379621925'

    def test_account_admin_user_str(self, admin_user):
        """
            Test the user string representation
        """

        assert admin_user.is_active is True
        assert admin_user.is_superuser is True
        assert admin_user.is_admin is True
        assert admin_user.__str__() == '09192311248'

    def test_account_user_phone_number_no_input(self, user_factory):
        """
            Test error with user not phone_number
        """

        with pytest.raises(ValueError) as e:
            user_factory.create(phone_number='')

        assert str(e.value) == 'The given phone must be set'

    def test_account_user_phone_number_incorrect(self, user_factory):
        """
            Test error with incorrect value in phone_number
        """

        with pytest.raises(ValueError) as e:
            user_factory.create(phone_number='1234')

        assert str(e.value) == 'You must enter correct format.'

    def test_account_admin_user_not_is_admin(self, user_factory):
        """
            Test error when admin is_admin=False
        """

        with pytest.raises(ValueError) as e:
            user_factory.create(phone_number='', is_superuser=True, is_active=True, is_admin=False)

        assert str(e.value) == 'Superuser must be assigned to is_admin=True'

    def test_account_admin_user_not_is_superuser(self, user_factory):
        """
            Test error when admin is_admin=False
        """

        with pytest.raises(ValueError) as e:
            user_factory.create(phone_number='', is_active=True, is_admin=True, is_superuser=False)

        assert str(e.value) == 'Superuser must be assigned to is_superuser=True'

    def test_account_admin_user_not_is_active(self, user_factory):
        """
            Test error when admin is_admin=False
        """

        with pytest.raises(ValueError) as e:
            user_factory.create(phone_number='', is_superuser=True, is_admin=True, is_active=False)

        assert str(e.value) == 'Superuser must be assigned to is_active=True'

    @pytest.mark.parametrize(
        'phone_number, email, full_name, validity',
        [
            ('09192311248', 'mohammadhssn@email.com', 'mohammdahssn A', 1),
            # ('12345', 'test@email.com', 'test', 0),
            # ('09352311268', '', '', 1),
            ('09352311268', '', '', 1),
            # ('09192311248', 'mohammadhssn@email.com', 'mohammdahssn A', 0),
        ]
    )
    def test_account_user_instance(self, db, user_factory, phone_number, email, full_name, validity):
        """
            Test create a new user instance
        """

        user_factory.create(
            phone_number=phone_number,
            email=email,
            full_name=full_name,
        )

        users = get_user_model().objects.all().count()

        assert users == validity

    @pytest.mark.parametrize(
        'phone_number, email, full_name',
        [
            ('12345', 'test@email.com', 'test'),
            ('091923112481234', 'mohammadhssn@email.com', 'mohammdahssn A'),
        ]
    )
    def test_account_user_instance_incorrect_value(self, db, user_factory, phone_number, email, full_name):
        """
            Test error create a new user instance with incorrect value
        """
        with pytest.raises(ValueError) as e:
            user_factory.create(
                phone_number=phone_number,
                email=email,
                full_name=full_name,
            )

        assert str(e.value) == 'You must enter correct format.'


class TestOtpCodeModel:

    def test_account_otp_code_string_representation(self, otp_code):
        """
            Test the otp_code sting representation
        """

        assert otp_code.__str__() == '09192311248'

    def test_account_create_otp(self, db, otp_code_factory):
        """
            Test create otp_code
        """

        random_code = random.randint(100000, 999999)
        otp_code = otp_code_factory.create(code=random_code, phone_number='09352311268')

        assert otp_code.code == random_code
        assert otp_code.phone_number == '09352311268'


class TestAddressModel:

    def test_account_address_string_representation(self, db, address_factory):
        """
            Test the address string representation
        """

        address = address_factory.create(full_name='mohammadhssn A')

        assert address.__str__() == 'mohammadhssn A Address'

    @pytest.mark.parametrize(
        'full_name, phone, postcode, address_line, address_line2, town_city, delivery_instructions,default',
        [
            ('mohammadhssn A', '09192331248', '12345', 'iran', 'iran', 'shahrood', 'nothing', True),
            ('sara irani', '09330238044', '12345', 'usa', 'usa', 'washengton', 'nothing', False),
        ]
    )
    def test_account_create_address(self, db, user_factory, address_factory, full_name, phone, postcode, address_line,
                                    address_line2, town_city, delivery_instructions, default):
        """
            Test create instance of address model
        """

        user = user_factory.create(phone_number='09192311248')

        address = address_factory.create(
            customer=user,
            full_name=full_name,
            phone=phone,
            postcode=postcode,
            address_line=address_line,
            address_line2=address_line2,
            town_city=town_city,
            delivery_instructions=delivery_instructions,
            default=default
        )

        all_address = Address.objects.count()

        assert address.full_name == full_name
        assert address.phone == phone
        assert address.postcode == postcode
        assert address.address_line == address_line
        assert address.town_city == town_city
        assert address.delivery_instructions == delivery_instructions
        assert address.default == default
        assert all_address == 1
