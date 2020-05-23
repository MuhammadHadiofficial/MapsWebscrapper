# Generated by Django 3.0.4 on 2020-05-21 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0010_business_area'),
    ]

    operations = [
        migrations.CreateModel(
            name='Orders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('orderID', models.CharField(blank=True, max_length=255, null=True, verbose_name='orderID')),
                ('email', models.CharField(blank=True, max_length=255, null=True, verbose_name='email')),
                ('company_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='company')),
                ('keyword', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('amount', models.CharField(blank=True, max_length=255, null=True)),
                ('status', models.CharField(blank=True, max_length=255, null=True)),
                ('address', models.CharField(blank=True, max_length=555, null=True)),
            ],
        ),
    ]