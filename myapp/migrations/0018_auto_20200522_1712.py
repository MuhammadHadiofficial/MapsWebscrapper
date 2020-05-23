# Generated by Django 3.0.4 on 2020-05-22 17:12

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0017_auto_20200522_1300'),
    ]

    operations = [
        migrations.AddField(
            model_name='orders',
            name='net_price',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='orders',
            name='orderDate',
            field=models.DateField(default=datetime.datetime(2020, 5, 22, 17, 12, 41, 274444, tzinfo=utc)),
        ),
    ]