from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

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
        Create otpcode for login wuth phone number
    """
    phone_number = models.CharField(
        max_length=12, validators=[phone_regex], verbose_name=_("phone"),
    )
    code = models.CharField(max_length=6)
    verify = models.BooleanField(default=False, verbose_name=_("is verify"))
    created = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.phone_number
