# Generated by Django 5.1.3 on 2024-11-21 08:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Restaurants', '0005_cart_cartitem'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitem',
            name='cart',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='customer',
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='dish',
        ),
        migrations.DeleteModel(
            name='Cart',
        ),
        migrations.DeleteModel(
            name='CartItem',
        ),
    ]
