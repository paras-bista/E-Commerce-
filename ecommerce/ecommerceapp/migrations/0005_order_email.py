# Generated by Django 5.1.5 on 2025-05-21 12:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceapp', '0004_remove_order_price_remove_order_product_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
