from django.contrib import admin
from mptt.admin import MPTTModelAdmin

from .models import (
    Category,
    Product,
    ProductType,
    ProductAttribute,
    ProductInventory,
    ProductAttributeValue,
    ProductTypeAttribute,
    ProductAttributeValues,
    Brand,
    Stock,
    Media
)

# ======================================================
admin.site.register(Category, MPTTModelAdmin)


# ======================================================
class ProductTypeAttributeInline(admin.TabularInline):
    model = ProductTypeAttribute


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = (ProductTypeAttributeInline,)


# ======================================================
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    pass


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductAttribute)
class ProductAttributeAdmin(admin.ModelAdmin):
    pass


@admin.register(ProductAttributeValue)
class ProductAttributeValueInline(admin.ModelAdmin):
    pass


# ======================================================
class ProductAttributeValuesInline(admin.TabularInline):
    model = ProductAttributeValues


class ProductMediaInline(admin.TabularInline):
    model = Media


@admin.register(ProductInventory)
class ProductInventoryAdmin(admin.ModelAdmin):
    inlines = (ProductAttributeValuesInline, ProductMediaInline)
