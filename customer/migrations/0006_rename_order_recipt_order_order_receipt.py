# Generated by Django 5.1.3 on 2024-11-28 10:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0005_order_order_recipt'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='order_recipt',
            new_name='order_receipt',
        ),
    ]
