# Generated by Django 5.1.3 on 2024-11-27 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_alter_order_payment_status_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='payment_intent_id',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
