from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def create_user(self, phone_number, password, **extra_fields):
        """
            Create a new user with phone number
        """
        if not phone_number:
            raise ValueError('The given phone must be set')

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
