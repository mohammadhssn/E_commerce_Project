from django.urls import path

from . import views

app_name = 'catalogue'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('product-detail/<str:web_id>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('category/<slug:slug>/', views.CategoryListView.as_view(), name='category'),
]
