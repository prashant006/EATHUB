# Generated by Django 5.1.3 on 2024-11-27 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0002_remove_order_order_status_orderitem_item_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='payment_status',
            field=models.CharField(choices=[('PENDING', 'Pending'), ('SUCCESS', 'Success'), ('REFUNDED', 'Refunded')], default='PENDING', max_length=10),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='item_image',
            field=models.ImageField(blank=True, null=True, upload_to='order_item_images/'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order_status',
            field=models.CharField(choices=[('PLACED', 'Placed'), ('ACCEPT', 'Accept'), ('ON_THE_WAY', 'On_the_way'), ('DELIVERED', 'Delivered'), ('CANCELLED', 'Cancelled')], default='PLACED', max_length=10),
        ),
    ]
