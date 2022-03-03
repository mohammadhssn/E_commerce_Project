from django.urls import path

from . import views

app_name = 'basket'

urlpatterns = [
    path('', views.BasketSummaryView.as_view(), name='basket_summary'),
    path('basket-add/', views.BasketAddView.as_view(), name='basket_add'),
    path('basket-delete/', views.BasketDeleteView.as_view(), name='basket_delete'),
    path('basket-update/', views.BasketUpdateView.as_view(), name='basket_update'),
]
