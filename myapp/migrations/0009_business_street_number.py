# Generated by Django 3.0.5 on 2020-05-10 21:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0008_auto_20200509_1011'),
    ]

    operations = [
        migrations.AddField(
            model_name='business',
            name='street_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
