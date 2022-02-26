import factory
import pytest
from faker import Faker

from django.contrib.auth import get_user_model

from apps.account.models import OtpCode

fake = Faker()


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
