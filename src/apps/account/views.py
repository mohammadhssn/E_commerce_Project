import random

from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model, login, authenticate

from .models import OtpCode
from .forms import UserRegistrationForm, VerifyCodeForm, UserLoginForm
from apps.utils import send_otp_code


class Register(View):
    form_class = UserRegistrationForm
    template_name = 'account/registration/register.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            phone = form.cleaned_data.get('phone')
            password1 = form.cleaned_data.get('password1')
            password2 = form.cleaned_data.get('password2')

            random_code = random.randint(100000, 999999)
            random_code = str(random_code)
            send_otp_code(phone, random_code)
            OtpCode.objects.create(phone_number=phone, code=random_code)
            print('*' * 90)
            print(form.cleaned_data['phone'])
            print(random_code)
            request.session['user_registration_info'] = {
                'phone_number': phone,
                'password1': password1,
                'password2': password2,
            }
            messages.success(request, _('we sent you a code'), 'success')
            return redirect('account:verify')
        return render(request, self.template_name, {'form': form})


class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm
    template_name = 'account/registration/verify.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        user_session = request.session.get('user_registration_info')
        try:
            code_instance = get_object_or_404(OtpCode, phone_number=user_session.get('phone_number'))
        except OtpCode.MultipleObjectsReturned:
            query = OtpCode.objects.filter(phone_number=user_session.get('phone_number'))
            code_instance = query.last()
            query.exclude(code=code_instance.code).delete()

        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd.get('code') == code_instance.code:
                user = get_user_model().objects.create_user(phone_number=user_session.get('phone_number'),
                                                            password=user_session.get('password1'))

                user.is_active = True
                user.save()
                login(request, user)
                code_instance.delete()
                messages.success(request, _('you registered. and loggen in successfully'), 'success')
                return redirect('catalogue:home')
            else:
                messages.error(request, _('this code is wrong'), 'danger')
                return redirect('account:verify')

        return redirect('catalogue:home')


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'account/registration/login.html'

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            phone = form.cleaned_data.get('phone')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=phone, password=password)
            print('*' * 90)
            print(user)
            if user is not None:
                login(request, user)
                messages.success(request, _('you logged in successfully'), 'success')
                return redirect('catalogue:home')
            else:
                messages.error(request, _('wrong phone or password'), 'warning')
                return redirect('account:login')
        else:
            return render(request, self.template_name, {'form': form})
