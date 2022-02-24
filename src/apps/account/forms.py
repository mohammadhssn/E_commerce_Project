from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password

from django.contrib.auth import get_user_model

from .models import phone_regex


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label=_('password'), validators=[validate_password], widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('confirm password'), widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ('phone_number', 'email', 'full_name')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError(_('passwords dont match'))
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text=_("you can change password using <a href=\"../password/\">this form</a>."))

    class Meta:
        model = get_user_model()
        fields = ('email', 'phone_number', 'full_name', 'password', 'last_login')


class UserRegistrationForm(forms.Form):
    phone = forms.CharField(label=_('Phone'), max_length=12, validators=[phone_regex])
    password1 = forms.CharField(label=_('password'), validators=[validate_password], widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('confirm password'), widget=forms.PasswordInput)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password1') and cd.get('password2') and cd.get('password1') != cd.get('password2'):
            raise ValidationError(_('passwords dont match'))
        return cd.get('password2')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        user = get_user_model().objects.filter(phone_number=phone)
        if user:
            raise ValidationError(_('phone is already! try another phone number'))
        return phone


class VerifyCodeForm(forms.Form):
    code = forms.CharField(max_length=6)


class UserLoginForm(forms.Form):
    phone = forms.CharField(label=_('Phone'), max_length=12, validators=[phone_regex])
    password = forms.CharField(label=_('password'), widget=forms.PasswordInput)
