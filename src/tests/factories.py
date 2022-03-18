import factory
import pytest
from faker import Faker

from django.contrib.auth import get_user_model

from apps.account.models import OtpCode, Address
from apps.catalogue.models import (
    Category,
    Product,
    ProductType,
    Brand,
    ProductInventory,
    Media,
    Stock,
    ProductAttribute, ProductAttributeValue, ProductAttributeValues
)
from apps.checkout.models import DeliveryOption, PaymentSelections
from apps.orders.models import Order, OrderItem, Coupon

fake = Faker()


# app account

class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = get_user_model()
        django_get_or_create = ('phone_number',)

    phone_number = '09379621925'
    password = fake.password()
    email = 'test@email.com'
    full_name = 'fname_lname'
    is_active = False
    is_admin = False

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        manager = cls._get_manager(model_class)
        if 'is_superuser' in kwargs:
            return manager.create_superuser(*args, **kwargs)
        else:
            return manager.create_user(*args, **kwargs)


class OtpCodeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OtpCode

    phone_number = '09192311248'
    code = '123456'


class AddressFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Address

    customer = factory.SubFactory(UserFactory)
    full_name = 'test full name'
    phone = '09192311248'
    postcode = '12345'
    address_line = 'address line 1'
    address_line2 = 'address line 2'
    town_city = 'iran'
    delivery_instructions = 'delivery_instructions'
    default = False


# =============================================================================
# app catalogue

# Category
class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.Sequence(lambda n: 'cat_name_%d' % n)
    slug = factory.Sequence(lambda n: 'slug_name_%d' % n)


# Product
class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product

    web_id = factory.Sequence(lambda n: 'web_id_%d' % n)
    slug = fake.lexify(text='prod_slug_??????')
    name = fake.lexify(text='prod_name_??????')
    description = fake.text()
    is_active = True
    created_at = '2021-09-04 22:14:18.279092'
    updated_at = '2021-09-04 22:14:18.279092'

    @factory.post_generation
    def category(self, create, extracted, **kwargs):
        if not create or not extracted:
            return
        if extracted:
            for cat in extracted:
                self.category.add(cat)


# ProductType
class ProductTypeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductType

    name = factory.Sequence(lambda n: "type_%d" % n)


# Brand
class BrandFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Brand

    name = factory.Sequence(lambda n: "brand_%d" % n)


# ProductInventory
class ProductInventoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductInventory

    sku = factory.Sequence(lambda n: "sku_%d" % n)
    upc = factory.Sequence(lambda n: "upc_%d" % n)
    product_type = factory.SubFactory(ProductTypeFactory)
    product = factory.SubFactory(ProductFactory)
    brand = factory.SubFactory(BrandFactory)
    is_active = 1
    retail_price = 97
    store_price = 92
    sale_price = 46
    weight = 987


# Media
class MediaFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Media

    product_inventory = factory.SubFactory(ProductInventoryFactory)
    image = 'default.png'
    alt_text = 'a default image solid color'
    is_feature = True


# Stock
class StockFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Stock

    product_inventory = factory.SubFactory(ProductInventoryFactory)
    units = 2
    units_sold = 100


# ProductAttribute
class ProductAttributeFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductAttribute

    name = factory.Sequence(lambda n: "attribute_name_%d" % n)
    description = factory.Sequence(lambda n: "description_%d" % n)


# ProductAttributeValue
class ProductAttributeValueFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductAttributeValue

    product_attribute = factory.SubFactory(ProductAttributeFactory)
    attribute_value = fake.lexify(text="attribute_value_??????")


# ProductAttributeValues
class ProductAttributeValuesFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = ProductAttributeValues

    attributevalues = factory.SubFactory(ProductAttributeValueFactory)
    productinventory = factory.SubFactory(ProductInventoryFactory)


# ProductAttributeValue
class ProductWithAttributeValuesFactory(ProductInventoryFactory):
    attributevalues1 = factory.RelatedFactory(
        ProductAttributeValuesFactory,
        factory_related_name="productinventory",
    )
    attributevalues2 = factory.RelatedFactory(
        ProductAttributeValuesFactory,
        factory_related_name="productinventory",
    )
    attributevalues3 = factory.RelatedFactory(
        ProductAttributeValuesFactory,
        factory_related_name="productinventory",
    )


# =============================================================================
# app checkout

class DeliveryOptionFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = DeliveryOption

    delivery_name = fake.text()
    delivery_price = 10000
    delivery_method = 'DD'
    delivery_timeframe = '0 days'
    delivery_window = fake.text()
    order = 1
    is_active = True


class PaymentSelectionsFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PaymentSelections

    name = fake.text()


# =============================================================================
# app orders

class OrderFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Order

    user = factory.SubFactory(UserFactory)
    full_name = 'full name'
    email = 'email@email.com'
    address = 'address line'
    city = 'shahrood'
    phone = '09192311248'
    postal_code = '123456'
    total_paid = 99000
    order_key = '124566'
    payment_option = 'payment option'
    billing_status = False
    discount = 0


class OrderItemFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = OrderItem

    order = factory.SubFactory(OrderFactory)
    product = factory.SubFactory(ProductInventoryFactory)
    price = 90000
    quantity = 1


class CouponFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Coupon

    code = 'ABC'
    valid_from = '2022-03-18 17:18:29.279092'
    valid_to = '2022-03-19 17:18:29.279092'
    discount = 50
    active = True
