from django.contrib.auth.models import BaseUserManager
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError

phone_regex = RegexValidator(
    regex=r"^(?:98|\+98|0098|0)?9[0-9]{9}$", message=_("Invalid phone number.")
)


class UserManager(BaseUserManager):

    def validate_phone_number(self, phone_number):
        try:
            phone_regex(phone_number)
        except ValidationError:
            raise ValueError(_('You must enter correct format.'))

    def create_user(self, phone_number, password, **extra_fields):
        """
            Create a new user with phone number
        """
        if phone_number:
            self.validate_phone_number(phone_number)
        else:
            raise ValueError(_('The given phone must be set'))

        user = self.model(phone_number=phone_number, **extra_fields)
        email = extra_fields.get('email')
        if email:
            user.email = self.normalize_email(email)
            print('*' * 90)
            print(email)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, password, **extra_fields):
        """
            Create a superuser with phone number
        """
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_admin') is not True:
            raise ValueError(_('Superuser must be assigned to is_admin=True'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must be assigned to is_superuser=True'))
        if extra_fields.get('is_active') is not True:
            raise ValueError(_('Superuser must be assigned to is_active=True'))

        return self.create_user(phone_number, password, **extra_fields)
