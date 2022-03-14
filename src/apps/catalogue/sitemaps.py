from django.contrib.sitemaps import Sitemap
from django.shortcuts import reverse

from .models import Category, Product


class StaticSitemapView(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return ['catalogue:home']

    def location(self, item):
        return reverse(item)


class CategorySitemapView(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return Category.objects.all()


class ProductSitemapView(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return Product.objects.all()
