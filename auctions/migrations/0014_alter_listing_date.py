# Generated by Django 4.1.3 on 2022-12-06 14:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_alter_listing_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='date',
            field=models.DateField(blank=True, default=datetime.datetime(2022, 12, 6, 14, 23, 37, 342391)),
        ),
    ]
