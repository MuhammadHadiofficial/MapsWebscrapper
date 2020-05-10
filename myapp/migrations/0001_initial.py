# Generated by Django 3.0.5 on 2020-05-06 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Business',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='name')),
                ('rating', models.CharField(blank=True, max_length=255, verbose_name='rating')),
                ('reviews', models.CharField(blank=True, max_length=255, verbose_name='reviews')),
                ('industry', models.CharField(blank=True, max_length=255)),
                ('street', models.CharField(blank=True, max_length=255)),
                ('city', models.CharField(blank=True, max_length=255)),
                ('country', models.CharField(blank=True, max_length=255)),
                ('opening_hours', models.CharField(blank=True, max_length=255)),
                ('phone_number', models.CharField(blank=True, max_length=255)),
                ('website', models.CharField(blank=True, max_length=255)),
            ],
        ),
    ]