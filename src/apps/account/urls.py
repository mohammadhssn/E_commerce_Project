from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('register/', views.Register.as_view(), name='register'),
    path('verify_code/', views.UserRegisterVerifyCodeView.as_view(), name='verify'),
    path('login/', views.UserLoginView.as_view(), name='login'),
]
