# Generated by Django 3.0.4 on 2020-05-25 17:09

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0019_auto_20200525_1641'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='orderDate',
            field=models.DateField(default=datetime.datetime(2020, 5, 25, 17, 9, 0, 316941, tzinfo=utc)),
        ),
        migrations.AlterUniqueTogether(
            name='business',
            unique_together=set(),
        ),
    ]
