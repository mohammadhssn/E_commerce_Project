from django.urls import path

from . import views

app_name = 'orders'

urlpatterns = [
    path('order-create/', views.CreateOrderView.as_view(), name='order_create'),
    path('payment-successfully/', views.PaymentSuccessfulView.as_view(), name='payment_success'),
    path('payment-selection/<int:order_id>/', views.PaymentSelectionView.as_view(), name='payment_selection'),
    path('apply-coupon/<int:order_id>/', views.ApplyCouponView.as_view(), name='apply_coupon'),
    path('delete-coupon/<int:order_id>/', views.RemoveCouponView.as_view(), name='delete_coupon'),

]
