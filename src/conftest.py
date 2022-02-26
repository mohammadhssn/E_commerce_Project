import pytest
from pytest_factoryboy import register

from tests.factories import (
    UserFactory,
    OtpCodeFactory
)

register(UserFactory)
register(OtpCodeFactory)


# User Fixture
@pytest.fixture
def user(db, user_factory):
    user = user_factory.create()
    return user


@pytest.fixture
def admin_user(db, user_factory):
    user = user_factory.create(phone_number='09192311248', is_superuser=True, is_admin=True, is_active=True)
    return user


# #############################################################################################################
# OtpCode Fixture
@pytest.fixture
def otp_code(db, otp_code_factory):
    otp_code = otp_code_factory.create()
    return otp_code
