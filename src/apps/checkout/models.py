from django.db import models
from django.utils.translation import gettext_lazy as _


class DeliveryOption(models.Model):
    """
        The Delivery methods table containing all delivery
    """

    DELIVERY_CHOICES = [
        ('IS', 'In Store'),
        ('HD', 'Home Delivery'),
        ('DD', 'Digital Delivery'),
    ]

    delivery_name = models.CharField(
        max_length=255,
        verbose_name=_('delivery_name'),
        help_text=_('format: required')
    )
    delivery_price = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name=_('delivery price'),
        help_text=_('Maximum 999.99'),
        error_messages={
            'name': {
                'max_length': _('The price must be between 0 and 999.'),
            },
        }
    )
    delivery_method = models.CharField(
        max_length=255,
        choices=DELIVERY_CHOICES,
        verbose_name=_('delivery_method'),
        help_text=_('format: required')
    )
    delivery_timeframe = models.CharField(
        max_length=255,
        verbose_name=_('delivery timeframe'),
        help_text=_('format: required')
    )
    delivery_window = models.CharField(
        max_length=255,
        verbose_name=_('delivery window'),
        help_text=_('format: required')
    )
    order = models.IntegerField(
        default=0,
        verbose_name=_('list order'),
        help_text=_('format: required')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('is_active'),
        help_text=_('in visible?')
    )

    class Meta:
        verbose_name = _("Delivery Option")
        verbose_name_plural = _("Delivery Options")

    def __str__(self):
        return self.delivery_name


class PaymentSelections(models.Model):
    """
        Store payment options
    """

    name = models.CharField(
        max_length=255,
        verbose_name=_('Name'),
        help_text=_('format: required')
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('is_active'),
        help_text=_('in visible?')
    )

    class Meta:
        verbose_name = _("Payment Selection")
        verbose_name_plural = _("Payment Selections")

    def __str__(self):
        return self.name
