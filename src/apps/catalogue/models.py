from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField


class Category(MPTTModel):
    """
        Inventory Category table implemented with MPTT
    """

    name = models.CharField(
        max_length=100,
        null=False,
        unique=False,
        blank=False,
        verbose_name=_('category name'),
        help_text=_('format: required, max-100')
    )
    slug = models.SlugField(
        max_length=150,
        null=False,
        unique=True,
        blank=False,
        verbose_name=_('category safe URL'),
        help_text=_('format: required, max-100')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('is_active')
    )
    parent = TreeForeignKey(
        'self',
        on_delete=models.SET_NULL,
        related_name='children',
        null=True,
        blank=True,
        unique=False,
        verbose_name=_('parent of category'),
        help_text=_('format: not required')
    )
    is_sub = models.BooleanField(
        default=False,
        verbose_name=_('category is sub?')
    )

    class MPTTMeta:
        order_insertion_by = ('name',)

    class Meta:
        verbose_name = _('product category')
        verbose_name_plural = _('product categories')

    def get_absolute_url(self):
        return reverse('catalogue:category', args=[self.slug])

    def __str__(self):
        return self.name


class Product(models.Model):
    """
        Product detail table
    """

    web_id = models.CharField(
        max_length=50,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_('product website ID'),
        help_text=_('format: required, unique')
    )
    slug = models.SlugField(
        max_length=255,
        unique=False,
        null=False,
        blank=False,
        verbose_name=_('product safe URL'),
        help_text=_('format: required, letters, numbers, underscores or hyphens')
    )
    name = models.CharField(
        max_length=255,
        unique=False,
        null=False,
        blank=False,
        verbose_name=_('product name'),
        help_text=_('format: required, max-255')
    )
    description = models.TextField(
        unique=False,
        null=False,
        blank=False,
        verbose_name=_('product description'),
        help_text=_('format: required')
    )
    category = TreeManyToManyField(Category)
    is_active = models.BooleanField(
        unique=False,
        null=False,
        blank=False,
        default=True,
        verbose_name=_('product visibility'),
        help_text=_('format: true=product visible')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_('date product created'),
        help_text=_('format Y-m-d H:M:S')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('date product last updated'),
        help_text=_('format Y-m-d H:M:S')
    )

    users_wishlist = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='user_wishlist',
        blank=True
    )

    def get_absolute_url(self):
        return reverse('catalogue:product_detail', args=[self.web_id])

    def __str__(self):
        return self.name


class ProductType(models.Model):
    """
        Product type table
    """

    name = models.CharField(
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_('type of product'),
        help_text=_('format: required, unique, max-255')
    )
    product_type_attribute = models.ManyToManyField(
        'ProductAttribute',
        related_name='product_type_attribute',
        through='ProductTypeAttribute'
    )

    def __str__(self):
        return self.name


class Brand(models.Model):
    """
        Product brand table
    """

    name = models.CharField(
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_('brand name'),
        help_text=_('format: required, unique, max-255')
    )

    def __str__(self):
        return self.name


class ProductAttribute(models.Model):
    """
        Product attribute table
    """

    name = models.CharField(
        max_length=255,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_('product attribute name'),
        help_text=_('format: required, unique, max-255')
    )
    description = models.TextField(
        unique=False,
        null=False,
        blank=False,
        verbose_name=_('product attribute description'),
        help_text=_('format: required')
    )

    def __str__(self):
        return self.name


class ProductAttributeValue(models.Model):
    """
        Product attribute value table
    """

    product_attribute = models.ForeignKey(
        ProductAttribute,
        related_name='product_attribute',
        on_delete=models.CASCADE
    )
    attribute_value = models.CharField(
        max_length=255,
        unique=False,
        null=False,
        blank=False,
        verbose_name=_('attribute value'),
        help_text=_('format: required, max-255')
    )

    def __str__(self):
        return f'{self.product_attribute.name} : {self.attribute_value}'


class ProductInventoryManger(models.Manager):
    """
        create custom manager for return product -> us_default=True
    """

    def is_default(self):
        return self.filter(is_default=True)


class ProductInventory(models.Model):
    """
        Product inventory table
    """

    sku = models.CharField(
        max_length=25,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_('stock keeping unit'),
        help_text=_('format: required, unique, max-20')
    )
    upc = models.CharField(
        max_length=12,
        unique=True,
        null=False,
        blank=False,
        verbose_name=_('universal product code'),
        help_text=_('format: required, unique, max-12')
    )
    product_type = models.ForeignKey(
        ProductType,
        related_name='product_type',
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        related_name='product',
        on_delete=models.CASCADE
    )
    brand = models.ForeignKey(
        Brand,
        related_name='brand',
        on_delete=models.CASCADE
    )
    attribute_values = models.ManyToManyField(
        ProductAttributeValue,
        related_name='product_attribute_values',
        through='ProductAttributeValues'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('product visibility'),
        help_text=_('format: true=product visible')
    )
    is_default = models.BooleanField(
        default=False,
        verbose_name=_('default selection'),
        help_text=_('format: true=sub-product visible')
    )
    retail_price = models.IntegerField(
        unique=False,
        null=False,
        blank=False,
        verbose_name=_('recommended retail price'),
        help_text=_('format:price Toman'),
        error_messages={
            'name': {
                'max_length': _('the price must be positive')
            },
        }
    )
    store_price = models.IntegerField(
        unique=False,
        null=False,
        blank=False,
        verbose_name=_('regular store price'),
        help_text=_('format:price Toman'),
        error_messages={
            'name': {
                'max_length': _('the price must be positive')
            },
        }
    )
    sale_price = models.IntegerField(
        unique=False,
        null=False,
        blank=False,
        verbose_name=_('sale price'),
        help_text=_('format:price Toman'),
        error_messages={
            'name': {
                'max_length': _('the price must be positive')
            },
        }
    )
    weight = models.FloatField(
        unique=False,
        null=False,
        blank=False,
        verbose_name=_('product weight')
    )
    created_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('date sub-product created'),
        help_text=_('format: Y-m-d H:M:S')
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('date sub-product updated'),
        help_text=_('format: Y-m-d H:M:S')
    )

    objects = ProductInventoryManger()

    def __str__(self):
        return self.product.name


class Media(models.Model):
    """
        The product image table
    """

    product_inventory = models.ForeignKey(
        ProductInventory,
        on_delete=models.CASCADE,
        related_name='media_product_inventory'
    )
    image = models.ImageField(
        unique=False,
        null=False,
        blank=False,
        default='default.png',
        verbose_name=_('product image'),
        help_text=_('format: required, default-detail.png')
    )
    alt_text = models.CharField(
        max_length=255,
        unique=False,
        null=False,
        blank=False,
        verbose_name=_('alternative text'),
        help_text=_('format: required, max-255')
    )
    is_feature = models.BooleanField(
        default=False,
        verbose_name=_('product default image'),
        help_text=_('format: default=False, True=default image')
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        editable=False,
        verbose_name=_('date sub-product created')
    )
    update_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('date sub-product updated'),
        help_text=_('format: Y-m-d H:M:S')
    )

    class Meta:
        verbose_name = _('product image')
        verbose_name_plural = _('product images')


class Stock(models.Model):
    """
        Stock units product table
    """
    product_inventory = models.OneToOneField(
        ProductInventory,
        related_name='product_inventory',
        on_delete=models.CASCADE
    )
    test_checked = models.DateTimeField(
        unique=False,
        null=True,
        blank=True,
        verbose_name=_('inventory stock check date'),
        help_text=_('format: Y-m-d H:M:S null=Ture, blank=True')
    )
    units = models.IntegerField(
        default=0,
        unique=False,
        null=False,
        blank=False,
        verbose_name=_('units sold to data'),
        help_text=_('format: required, default=0')
    )
    units_sold = models.IntegerField(
        default=0,
        unique=False,
        null=False,
        blank=False,
        verbose_name=_("units sold to date"),
        help_text=_("format: required, default-0"),
    )


class ProductAttributeValues(models.Model):
    """
        Product attribute values link table
    """

    attributevalues = models.ForeignKey(
        ProductAttributeValue,
        related_name='attributevalues',
        on_delete=models.CASCADE
    )
    productinventory = models.ForeignKey(
        ProductInventory,
        related_name='productattibutevalues',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = (('attributevalues', 'productinventory'),)


class ProductTypeAttribute(models.Model):
    """
        Product type attribute link table
    """

    product_attribute = models.ForeignKey(
        ProductAttribute,
        related_name='productattribute',
        on_delete=models.CASCADE
    )
    product_type = models.ForeignKey(
        ProductType,
        related_name='producttype',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = (('product_attribute', 'product_type'),)
