"""config URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.contrib.sitemaps.views import sitemap

from apps.catalogue.sitemaps import StaticSitemapView, CategorySitemapView, ProductSitemapView

sitemaps = {
    'static': StaticSitemapView,
    'category': CategorySitemapView,
    'product': ProductSitemapView,
}

urlpatterns = [
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}),
    re_path(r'^robot\.txt$', include('robots.urls')),
    path('adminstartion@mohammadhssn78/', admin.site.urls),
    path('account/', include('apps.account.urls', namespace='account')),
    path('basket/', include('apps.basket.urls', namespace='basket')),
    path('checkout/', include('apps.checkout.urls', namespace='checkout')),
    path('oreders/', include('apps.orders.urls', namespace='orders')),
    path('', include('apps.catalogue.urls', namespace='catalogue')),

]

if settings.DEBUG:
    urlpatterns += path('__debug__/', include('debug_toolbar.urls')),
