# Generated by Django 4.0.2 on 2022-03-07 16:31

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('catalogue', '0005_stock_units_sold'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='users_wishlist',
            field=models.ManyToManyField(blank=True, related_name='user_wishlist', to=settings.AUTH_USER_MODEL),
        ),
    ]