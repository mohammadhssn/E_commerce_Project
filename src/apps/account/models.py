import uuid

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.conf import settings

from .managers import UserManager

phone_regex = RegexValidator(
    regex=r"^(?:98|\+98|0098|0)?9[0-9]{9}$", message=_("Invalid phone number.")
)


class User(AbstractBaseUser, PermissionsMixin):
    """
        Create Custom User
    """
    phone_number = models.CharField(
        max_length=12, unique=True, validators=[phone_regex], verbose_name=_('Phone number')
    )
    email = models.EmailField(max_length=255, blank=True, null=True, unique=True, verbose_name=_('Email Address'))
    full_name = models.CharField(
        max_length=100, blank=True, verbose_name=_("full name")
    )

    is_active = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(
        default=timezone.now, verbose_name=_("date joined")
    )

    objects = UserManager()
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['email', 'full_name']

    def __str__(self):
        return self.phone_number

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class OtpCode(models.Model):
    """
        Create otp_code for login with phone number
    """
    phone_number = models.CharField(
        max_length=12, validators=[phone_regex], verbose_name=_("phone"),
    )
    code = models.CharField(max_length=6, verbose_name=_('code'))
    created = models.DateTimeField(auto_now=True, verbose_name=_('created'))
    expire_time = models.DateTimeField(default=timezone.now, verbose_name=_('expire_time'))

    def __str__(self):
        return self.phone_number


class Address(models.Model):
    """
        Address Customer
    """

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    customer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name=_('Customer')
    )
    full_name = models.CharField(
        max_length=150,
        verbose_name=_('full name')
    )
    phone = models.CharField(
        max_length=12, validators=[phone_regex], verbose_name=_("phone"),
    )
    postcode = models.CharField(
        _('Postcode'),
        max_length=50
    )
    address_line = models.CharField(
        _('Address Line 1'),
        max_length=255
    )
    address_line2 = models.CharField(
        _('Address Line 2'),
        max_length=255
    )
    town_city = models.CharField(
        _('Town/City/State'),
        max_length=150
    )
    delivery_instructions = models.CharField(
        _('Delivery Instructions'),
        max_length=255
    )
    created_at = models.DateTimeField(
        _('Created at'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _('Updated at'),
        auto_now=True
    )
    default = models.BooleanField(
        _('Default'),
        default=False
    )

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    def __str__(self):
        return f"{self.full_name} Address"
