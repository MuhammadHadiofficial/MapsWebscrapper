# Generated by Django 3.0.4 on 2020-05-11 16:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0009_business_street_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='area',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
