# Generated by Django 5.1.3 on 2024-11-20 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Reviews', '0004_alter_review_restaurant'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='avg_rating',
            field=models.FloatField(default=0.0),
        ),
    ]
