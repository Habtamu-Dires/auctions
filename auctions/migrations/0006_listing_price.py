# Generated by Django 4.1.3 on 2022-12-06 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0005_alter_listing_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='price',
            field=models.FloatField(default=0.0),
        ),
    ]