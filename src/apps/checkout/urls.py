from django.urls import path

from . import views

app_name = 'checkout'

urlpatterns = [
    path('delivery-choices/', views.DeliveryChoicesView.as_view(), name='delivery_choices'),
    path('basket-update-delivery/', views.BasketUpdateDeliveryView.as_view(), name='basket_update_delivery'),
]
