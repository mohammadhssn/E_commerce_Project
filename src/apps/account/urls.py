from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('register/verify_code/', views.UserRegisterVerifyCodeView.as_view(), name='verify'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('forget-password/', views.ForgettingPasswordView.as_view(), name='forget_password'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset_password'),
    path("reset-password-done/", views.ResetPasswordDoneView.as_view(), name='reset_password_done'),
]
