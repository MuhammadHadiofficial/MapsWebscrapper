from django.db import models

from django.db import models


class Business(models.Model):
    name = models.CharField('name',blank=True, max_length=255,null=True)
    rating = models.CharField('rating',blank=True,max_length=255,null=True)
    reviews = models.CharField('reviews',blank=True,max_length=255,null=True)
    industry = models.CharField(blank=True,max_length=255,null=True)
    street = models.CharField(blank=True,max_length=255,null=True)
    street_number = models.CharField(blank=True,max_length=255,null=True)
    postalcode = models.CharField(blank=True,max_length=255,null=True)
    area = models.CharField(blank=True,max_length=255,null=True)

    city=models.CharField(blank=True,max_length=255,null=True)
    country=models.CharField(blank=True,max_length=255,null=True)
    opening_hours=models.CharField(blank=True,max_length=255,null=True)
    phone_number=models.CharField(blank=True,max_length=255,null=True)
    website=models.CharField(blank=True,max_length=255,null=True)
    keyword=models.CharField(blank=True,max_length=255,null=True)
    email=models.CharField(blank=True,max_length=255,null=True)
    class Meta:
        unique_together = [['name', 'industry','city','keyword','postalcode']]
# Create your models here.
