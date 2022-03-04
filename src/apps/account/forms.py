from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.password_validation import validate_password

from django.contrib.auth import get_user_model

from .models import phone_regex


class UserCreationForm(forms.ModelForm):
    """
        For create new user in admin-panel
    """
    password1 = forms.CharField(label=_('password'), validators=[validate_password], widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('confirm password'), widget=forms.PasswordInput)

    class Meta:
        model = get_user_model()
        fields = ('phone_number', 'email', 'full_name')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password1') and cd.get('password2') and cd.get('password1') != cd.get('password2'):
            raise ValidationError(_('passwords dont match'))
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """
        For update user in admin-panel
    """
    password = ReadOnlyPasswordHashField(
        help_text=_("you can change password using <a href=\"../password/\">this form</a>."))

    class Meta:
        model = get_user_model()
        fields = ('email', 'phone_number', 'full_name', 'password', 'last_login')


# @@@@@@@@@@@@@@@@@
class UserRegistrationForm(forms.Form):
    """
        For create new user with phone-number
    """
    phone = forms.CharField(label=_('Phone'), max_length=12, validators=[phone_regex])
    password = forms.CharField(label=_('password'), validators=[validate_password], widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('confirm password'), widget=forms.PasswordInput)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') and cd.get('password2') and cd.get('password') != cd.get('password2'):
            raise ValidationError(_('passwords dont match'))
        return cd.get('password2')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        user = get_user_model().objects.filter(phone_number=phone)
        if user:
            raise ValidationError(_('phone is already! try another phone number'))
        return phone

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'phone'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password'})


class VerifyCodeForm(forms.Form):
    """
        get code for complete registry
    """
    code = forms.CharField(max_length=6)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['code'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'code'}
        )


class UserLoginForm(forms.Form):
    """
        login a user
    """
    phone = forms.CharField(label=_('Phone'), max_length=12, validators=[phone_regex])
    password = forms.CharField(label=_('password'), widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'phone'})
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})


class ForgettingPasswordForm(forms.Form):
    """
        get phone_number for reset_password
    """
    phone = forms.CharField(label=_('Phone'), max_length=12, validators=[phone_regex])

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        try:
            get_user_model().objects.get(phone_number=phone)
        except get_user_model().DoesNotExist:
            raise ValidationError(_('Account not Found! try again Or Register to site'))
        return phone

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['phone'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'phone'})


class VerifyCodePasswordForm(VerifyCodeForm):
    """
        get code for complete reset password
        Inherit from VerifyCodeForm
    """
    pass


class RestPasswordDoneForm(forms.Form):
    """
        Change password completely
    """
    password = forms.CharField(label=_('password'), validators=[validate_password], widget=forms.PasswordInput)
    password2 = forms.CharField(label=_('confirm password'), widget=forms.PasswordInput)

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password') and cd.get('password2') and cd.get('password') != cd.get('password2'):
            raise ValidationError(_('passwords dont match'))
        return cd.get('password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password'].widget.attrs.update(
            {'class': 'form-control mb-3', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update(
            {'class': 'form-control', 'placeholder': 'Repeat Password'})


# Profile
class UserEditProfileForm(forms.ModelForm):
    phone_number = forms.CharField(
        label=_('Phone Number (can not be changed)'),
        max_length=12,
        widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'phone', 'id': 'form-phone', 'readonly': 'readonly'}
        ))
    full_name = forms.CharField(
        label=_('Username'), min_length=3, max_length=50, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'Username', 'id': 'form-firstname'}))

    email = forms.EmailField(
        label=_('Account email'), max_length=200, widget=forms.TextInput(
            attrs={'class': 'form-control mb-3', 'placeholder': 'email', 'id': 'form-email'}
        ))

    class Meta:
        model = get_user_model()
        fields = ('phone_number', 'full_name', 'email')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['full_name'].required = True
        self.fields['email'].required = True
