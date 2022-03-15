from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from apps.catalogue.models import ProductInventory, Product


@registry.register_document
class ProductInventoryDocument(Document):
    product = fields.ObjectField(
        properties={
            'name': fields.TextField(),
            'web_id': fields.TextField()
        }
    )
    media_product_inventory = fields.ObjectField(
        properties={
            'image': fields.FileField(),
            'alt_text': fields.TextField(),
            'is_feature': fields.BooleanField()
        }
    )

    class Index:
        name = 'productinventory'

    class Django:
        model = ProductInventory
        fields = ('id', 'is_default', 'store_price')
