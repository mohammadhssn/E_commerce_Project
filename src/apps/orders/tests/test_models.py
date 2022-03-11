import pytest

from ..models import Order, OrderItem


class TestOrderModel:

    def test_orders_db_category_insert_data(self, db, order_factory):
        """
            Test create instance of Order model
        """

        order = order_factory.create(billing_status=True)
        count_order = Order.objects.count()

        assert order.full_name == 'full name'
        assert order.email == 'email@email.com'
        assert order.address == 'address line'
        assert order.city == 'shahrood'
        assert order.order_key == '124566'
        assert order.phone == '09192311248'
        assert order.postal_code == '123456'
        assert order.payment_option == 'payment option'
        assert order.billing_status is True
        assert order.__str__() == f'{order.user} : {order.created}'
        assert count_order == 1


class TestOrderItemModel:
    def test_orders_db_category_insert_data(self, db, product_inventory_factory, order_factory, order_item_factory):
        """
            Test create instance of OrderItem model
        """

        order = order_factory.create()
        product = product_inventory_factory.create()
        order_item = order_item_factory.create(order=order, product=product)
        count_order_item = OrderItem.objects.count()

        assert order_item.price == 90.00
        assert order_item.quantity == 1
        assert count_order_item == 1
        assert order_item.__str__() == f'{order_item.order.user} : {str(order_item.pk)}'
