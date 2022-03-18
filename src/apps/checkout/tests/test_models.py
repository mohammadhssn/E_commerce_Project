import pytest

from ..models import DeliveryOption, PaymentSelections


class TestDeliveryOptionModel:

    @pytest.mark.parametrize(
        'delivery_name, delivery_price, delivery_method, delivery_timeframe, delivery_window, order',
        [
            ('post_express', '10000', 'IS', '3 days', 'test_window', 1),
            ('post_airport', '20000', 'HD', '2 days', 'test_window', 2),
            ('post', '0', 'DD', 'now', 'test_window', 1),
        ]
    )
    def test_checkout_db_delivery_option_insert_data(self, db, delivery_option_factory, delivery_name, delivery_price,
                                                     delivery_method, delivery_timeframe, delivery_window, order):
        """
            Test create new objects delivery_option
        """

        result = delivery_option_factory.create(
            delivery_name=delivery_name,
            delivery_price=delivery_price,
            delivery_method=delivery_method,
            delivery_timeframe=delivery_timeframe,
            delivery_window=delivery_window,
            order=order
        )

        all_delivery_options = DeliveryOption.objects.count()

        assert all_delivery_options == 1
        assert result.delivery_name == delivery_name
        assert result.delivery_price == delivery_price
        assert result.delivery_method == delivery_method
        assert result.delivery_timeframe == delivery_timeframe
        assert result.delivery_window == delivery_window
        assert result.order == order
        assert result.__str__() == delivery_name


class TestPaymentSelectionModel:

    def test_checkout_db_delivery_option_insert_data(self, db, payment_selections_factory):
        """
            Test create new objects delivery_option
        """

        result = payment_selections_factory.create(
            name='test payment selection',

        )

        all_payment_selection = PaymentSelections.objects.count()

        assert all_payment_selection == 1
        assert result.name == 'test payment selection'
        assert result.__str__() == 'test payment selection'
