# Generated by Django 5.1.5 on 2025-05-21 12:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerceapp', '0005_order_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_proof',
            field=models.ImageField(blank=True, null=True, upload_to='payment_proofs/'),
        ),
    ]
