# Generated by Django 3.0.4 on 2020-05-22 12:39

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0015_auto_20200522_1239'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='orderDate',
            field=models.DateField(default=datetime.datetime(2020, 5, 22, 12, 39, 12, 99506, tzinfo=utc)),
        ),
    ]
