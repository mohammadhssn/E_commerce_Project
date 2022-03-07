from django.urls import path

from . import views

app_name = 'account'

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('register/verify_code/', views.UserRegisterVerifyCodeView.as_view(), name='verify'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # reset password
    path('forget-password/', views.ForgettingPasswordView.as_view(), name='forget_password'),
    path('reset-password/', views.ResetPasswordView.as_view(), name='reset_password'),
    path("reset-password-done/", views.ResetPasswordDoneView.as_view(), name='reset_password_done'),
    # dashboard
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('edit-profile/', views.EditProfileView.as_view(), name='edit_profile'),
    # Address
    path('addresses/', views.AddressView.as_view(), name='addresses'),
    path('addresses/add/', views.AddAddressView.as_view(), name='add_addresses'),
    path('addresses/edit/<uuid:id>/', views.EditAddressView.as_view(), name='edit_addresses'),
    path('addresses/delete/<uuid:id>/', views.DeleteAddressView.as_view(), name='delete_addresses'),
    path('addresses/set-default/<uuid:id>/', views.SetDefaultAddressView.as_view(), name='set_default_addresses'),
    # Wash list
    path('washlist/', views.WashListView.as_view(), name='wash_list'),
    path('washlist/add-to-washlist/<int:id>/', views.AddWashListView.as_view(), name='add_wash_list'),
]
