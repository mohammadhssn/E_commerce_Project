import pytest
from django.db import IntegrityError

from apps.catalogue.models import (
    Category,
    Product, ProductInventory,
)


class TestCategoryModels:

    @pytest.mark.parametrize(
        'name, slug, is_active, is_sub',
        [
            ('fashion', 'fashion', 1, 0),
            ('trainers', 'trainers', 1, 0),
            ('baseball', 'baseball', 1, 1),
        ]
    )
    def test_catalogue_db_category_insert_data(self, db, category_factory, name, slug, is_active, is_sub):
        """
            Test create new category
        """

        result = category_factory.create(name=name, slug=slug, is_active=is_active, is_sub=is_sub)
        all_category = Category.objects.count()

        assert result.name == name
        assert result.slug == slug
        assert result.is_active == is_active
        assert result.is_sub == is_sub
        assert result.__str__() == name
        assert all_category == 1

    def test_catalogue_db_category_uniqueness_integrity(self, db, category_factory):
        """
            test error when create new category with already slug
        """
        category_factory.create(slug='cat_slug')
        with pytest.raises(IntegrityError):
            category_factory.create(slug='cat_slug')


class TestProductModels:

    @pytest.mark.parametrize(
        'id, web_id, name, slug, description, is_active, created_at, updated_at',
        [
            (
                    1,
                    '45425810',
                    'widstar running sneakers',
                    'widstar-running-sneakers',
                    'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin porta, eros vel sollicitudin lacinia, quam metus gravida elit, a elementum nisl neque sit amet orci. Nulla id lorem ac nunc cursus consequat vitae ut orci. In a velit eu justo eleifend tincidunt vel eu turpis. Praesent eu orci egestas, lobortis magna egestas, tincidunt augue. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Aenean vitae lectus eget tortor laoreet efficitur vel et leo. Maecenas volutpat eget ante id tempor. Etiam posuere ex urna, at aliquet risus tempor eu. Aenean a odio odio. Nunc consectetur lorem ante, interdum ultrices elit consectetur sit amet. Vestibulum rutrum interdum nulla. Cras vel mi a enim eleifend blandit. Curabitur ex dui, rutrum et odio sit amet, auctor euismod massa.',
                    1,
                    '2021-09-04 22:14:18',
                    '2021-09-04 22:14:18'
            ),
            (
                    8616,
                    '45434425',
                    'impact puse dance shoe',
                    'impact-puse-dance-shoe',
                    'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Proin porta, eros vel sollicitudin lacinia, quam metus gravida elit, a elementum nisl neque sit amet orci. Nulla id lorem ac nunc cursus consequat vitae ut orci. In a velit eu justo eleifend tincidunt vel eu turpis. Praesent eu orci egestas, lobortis magna egestas, tincidunt augue. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae; Aenean vitae lectus eget tortor laoreet efficitur vel et leo. Maecenas volutpat eget ante id tempor. Etiam posuere ex urna, at aliquet risus tempor eu. Aenean a odio odio. Nunc consectetur lorem ante, interdum ultrices elit consectetur sit amet. Vestibulum rutrum interdum nulla. Cras vel mi a enim eleifend blandit. Curabitur ex dui, rutrum et odio sit amet, auctor euismod massa.',
                    1,
                    '2021-09-04 22:14:18',
                    '2021-09-04 22:14:18'
            ),
        ]
    )
    def test_catalogue_db_product_insert_data(self, db, category_factory, product_factory, id, web_id, name, slug,
                                              description, is_active,
                                              created_at, updated_at):
        """
            test create new product
        """
        category_1 = category_factory.create(name='cat_1', slug='cat-1')
        category_2 = category_factory.create(name='cat_2', slug='cat-2')

        product = product_factory.create(
            id=id,
            web_id=web_id,
            name=name,
            slug=slug,
            category=(category_1.id, category_2.id),
            description=description,
            created_at=created_at,
            updated_at=updated_at
        )

        all_product_category = product.category.all().count()
        all_product = Product.objects.count()

        assert product.web_id == web_id
        assert product.name == name
        assert all_product_category == 2
        assert all_product == 1
        assert product.__str__() == name

    def test_catalogue_db_product_uniqueness_integrity(self, db, product_factory):
        """
            test error when create new product with already web_id
        """
        product_factory.create(web_id=12356789)
        with pytest.raises(IntegrityError):
            product_factory.create(web_id=12356789)


class TestProductTypeModels:

    def test_catalogue_db_product_type_insert_data(self, db, product_type_factory):
        """
            test create new product type
        """

        product_type = product_type_factory.create(name='demo_type')

        assert product_type.name == 'demo_type'
        assert product_type.__str__() == 'demo_type'

    def test_catalogue_db_product_type_uniqueness_integrity(self, db, product_type_factory):
        """
            test error when create new product_type with already name
        """
        product_type_factory.create(name='demo_type')

        with pytest.raises(IntegrityError):
            product_type_factory.create(name='demo_type')


class TestBrandModels:

    def test_catalogue_db_brand_insert_data(self, db, brand_factory):
        """
            test create new brand
        """

        brand = brand_factory.create(name='demo_brand')

        assert brand.name == 'demo_brand'
        assert brand.__str__() == 'demo_brand'

    def test_catalogue_db_brand_uniqueness_integrity(self, db, brand_factory):
        """
            test error when create new brand with already name
        """
        brand_factory.create(name='demo_brand')

        with pytest.raises(IntegrityError):
            brand_factory.create(name='demo_brand')


class TestProductInventoryModels:

    @pytest.mark.parametrize(
        "id, sku, upc, is_active, retail_price, store_price, sale_price, weight",
        [
            (
                    1,
                    "7633969397",
                    "934093051374",
                    1,
                    97.00,
                    92.00,
                    46.00,
                    987,
            ),
            (
                    8616,
                    "3880741573",
                    "844935525855",
                    1,
                    89.00,
                    84.00,
                    42.00,
                    929,
            ),
        ],
    )
    def test_catalogue_db_product_inventory_insert_data(
            self, db, product_inventory_factory, id, sku, upc,
            is_active, retail_price, store_price, sale_price, weight
    ):
        """
            test create new product inventory
        """
        # product = product_factory.create()
        # brand = brand_factory.create(name='test_brand')
        # product_type = product_type_factory.create(name='test_type')

        result = product_inventory_factory.create(
            id=id,
            sku=sku,
            upc=upc,
            product_type__name='test_brand',
            product__web_id='123456789',
            brand__name='test_type',
            is_active=is_active,
            retail_price=retail_price,
            store_price=store_price,
            sale_price=sale_price,
            weight=weight,

        )

        assert result.sku == sku
        assert result.upc == upc
        assert result.product_type.name == 'test_brand'
        assert result.product.web_id == '123456789'
        assert result.brand.name == 'test_type'
        assert result.is_active == is_active
        assert result.retail_price == retail_price
        assert result.store_price == store_price
        assert result.sale_price == sale_price
        assert result.weight == weight
        assert result.__str__() == result.product.name

    def test_catalogue_product_inventory_custom_manager_is_default(self, db, product_inventory_factory):
        """
            test custom manger is_default:
        """
        product_inventory_factory.create(is_default=False)
        product_inventory_factory.create(is_default=True)
        count = ProductInventory.objects.is_default().count()

        assert count == 1


class TestMediaModels:

    @pytest.mark.parametrize(
        'id, image, alt_text, is_feature',
        [
            (
                    1,
                    "default.png",
                    "a default image solid color",
                    1,
            ),
            (
                    8616,
                    "default.png",
                    "a default image solid color",
                    1,
            ),
        ],
    )
    def test_catalogue_db_media_insert_data(self, db, media_factory, id, image, alt_text, is_feature):
        """
            test create a new media
        """

        result = media_factory.create(
            id=id,
            product_inventory__sku='123456789',
            image=image,
            alt_text=alt_text,
            is_feature=is_feature
        )

        assert result.product_inventory.sku == '123456789'
        assert result.image == image
        assert result.alt_text == alt_text
        assert result.is_feature == is_feature


class TestStockModels:

    @pytest.mark.parametrize(
        'id, units, units_sold',
        [
            (1, 135, 0),
            (8616, 100, 0),
        ],
    )
    def test_catalogue_db_stock_insert_data(self, db, stock_factory, id, units, units_sold):
        """
            test create a new Stock
        """

        result = stock_factory.create(
            id=id,
            product_inventory__sku='123456789',
            units=units,
            units_sold=units_sold
        )

        assert result.product_inventory.sku == '123456789'
        assert result.id == id
        assert result.units == units
        assert result.units_sold == units_sold


class TestProductAttributeModels:

    @pytest.mark.parametrize(
        "id, name, description",
        [
            (1, "men-shoe-size", "men shoe size"),
        ],
    )
    def test_catalogue_db_product_attribute_insert_data(self, db, product_attribute_factory, id, name, description):
        """
            test create a new product attribute
        """

        result = product_attribute_factory.create(
            id=id,
            name=name,
            description=description,
        )

        assert result.id == id
        assert result.name == name
        assert result.description == description

    def test_catalogue_db_product_attribute_uniqueness_integrity(self, db, product_attribute_factory):
        """
            test error when create new brand with already name
        """
        product_attribute_factory.create(name='test_name')

        with pytest.raises(IntegrityError):
            product_attribute_factory.create(name='test_name')


class TestProductAttributeValueModels:

    def test_catalogue_db_product_attribute_value_insert_data(self, db, product_attribute_value_factory):
        """
            test create a new product attribute value
        """

        result = product_attribute_value_factory.create(
            attribute_value='new_value', product_attribute__name='new_attribute'
        )

        assert result.attribute_value == 'new_value'
        assert result.product_attribute.name == 'new_attribute'
        assert result.__str__() == f'{result.product_attribute.name} : {result.attribute_value}'


class TestProductAttributeValuesModels:

    def test_catalogue_db_product_attribute_values_insert_data(self, db, product_with_attribute_values_factory):
        """
            test create a new product attribute_values
        """

        new_in_attribute = product_with_attribute_values_factory(sku="123456789")

        result = ProductInventory.objects.get(sku="123456789")
        count = result.attribute_values.all().count()

        assert count == 3
