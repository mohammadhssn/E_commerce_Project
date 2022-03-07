from django.contrib.postgres.aggregates import ArrayAgg
from django.core.paginator import Paginator
from django.db.models import Count
from django.shortcuts import render, get_object_or_404
from django.views import View

from .models import ProductInventory, ProductTypeAttribute, Media, Category


class HomeView(View):

    def get(self, request):
        products = ProductInventory.objects.prefetch_related('media_product_inventory').filter(is_active=True)
        return render(request, 'catalogue/home.html', {'products': products})


class ProductDetailView(View):
    """
        Product detail view
    """

    template_name = 'catalogue/product_detail.html'

    def get(self, request, web_id=None):

        if request.GET:
            filter_arguments = []
            for value in request.GET.values():
                filter_arguments.append(value)

            product = ProductInventory.objects.filter(product__web_id=web_id).filter(
                attribute_values__attribute_value__in=filter_arguments).annotate(
                num_tags=Count('attribute_values')).filter(num_tags=len(filter_arguments)).values(
                "id", "sku", "product__name", "store_price", "product_inventory__units").annotate(
                field_a=ArrayAgg("attribute_values__attribute_value")).get()

        else:
            product = ProductInventory.objects.filter(
                product__web_id=web_id).filter(is_default=True).values(
                "id", "sku", "product__id", "product__name", "store_price", "product_inventory__units").annotate(
                field_a=ArrayAgg("attribute_values__attribute_value")).get()

        # must Change
        product_image = Media.objects.filter(
            product_inventory__product__web_id=web_id)

        product_attribute_values = ProductInventory.objects.filter(product__web_id=web_id).distinct().values(
            "attribute_values__product_attribute__name", "attribute_values__attribute_value")

        product_type_attributes = ProductTypeAttribute.objects.filter(
            product_type__product_type__product__web_id=web_id).distinct().values("product_attribute__name")

        return render(request, self.template_name,
                      {'product': product, 'product_attribute_values': product_attribute_values,
                       'product_type_attributes': product_type_attributes, 'product_image': product_image})


class CategoryListView(View):
    """
        List of Category
    """

    def get(self, request, slug=None):
        category = get_object_or_404(Category, slug=slug, is_active=True)
        products = ProductInventory.objects.is_default().filter(
            product__category__in=category.get_descendants(
                include_self=True)).distinct()

        paginator = Paginator(products, 10)  # Show 10 contacts per page.
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        return render(request, 'catalogue/category.html', {'category': category, 'page_obj': page_obj})
