import pytest

from ..forms import CouponForm


class TestCouponForm:

    @pytest.mark.parametrize(
        'code, validity',
        [
            ('ABC', True),
            ('sdfhgjhkhhd', True),
            ('', False),
        ]
    )
    def test_orders_check_coupon_form(self, db, code, validity):
        """
            Test for check coupon is valid or not
        """

        form = CouponForm(data={'code': code})

        assert form.is_valid() is validity
