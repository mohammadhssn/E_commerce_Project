from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('payment-complete/', views.PaymentCompleteView.as_view(), name='payment_complete'),
    path('payment-successfully/', views.PaymentSuccessfulView.as_view(), name='payment_success')

]
