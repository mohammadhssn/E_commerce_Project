import pytest
from pytest_factoryboy import register

from tests.factories import (
    UserFactory,
    OtpCodeFactory,
    CategoryFactory,
    ProductFactory,
    ProductTypeFactory,
    BrandFactory,
    ProductInventoryFactory,
    MediaFactory,
    StockFactory,
    ProductAttributeFactory,
    ProductAttributeValueFactory,
    ProductAttributeValuesFactory,
    ProductWithAttributeValuesFactory,
    DeliveryOptionFactory,
    PaymentSelectionsFactory,
    AddressFactory,
    OrderFactory,
    OrderItemFactory
)

register(UserFactory)
register(OtpCodeFactory)
register(AddressFactory)

register(CategoryFactory)
register(ProductTypeFactory)
register(ProductFactory)
register(BrandFactory)
register(ProductInventoryFactory)
register(MediaFactory)
register(StockFactory)
register(ProductAttributeFactory)
register(ProductAttributeValueFactory)
register(ProductAttributeValuesFactory)
register(ProductWithAttributeValuesFactory)

register(DeliveryOptionFactory)
register(PaymentSelectionsFactory)

register(OrderFactory)
register(OrderItemFactory)


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

# app account

# OtpCode Fixture
@pytest.fixture
def otp_code(db, otp_code_factory):
    otp_code = otp_code_factory.create()
    return otp_code


# Session [user_registration_info]
@pytest.fixture
def set_session_user_info(db, client):
    session = client.session
    session['user_registration_info'] = {
        'phone_number': '09192311248',
        'password': '@testpass1',
        'password2': '@testpass1',
    }
    session.save()
    yield session
    del session


@pytest.fixture
def set_session_reset_password(db, client):
    session = client.session
    session['user_forgetting_password'] = {
        'phone_number': '09192311248',
    }
    session.save()
    return session


# #############################################################################################################

# app checkout
@pytest.fixture
def set_session_purchase(db, client):
    session = client.session
    session['purchase'] = {
        'delivery_id': 1
    }
    session.save()
    return session


@pytest.fixture
def set_session_address(db, client):
    session = client.session
    session['address'] = {
        'address_id': 1
    }
    session.save()
    return session



