from django.db import models

from django.db import models
from django.utils import timezone

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
    # class Meta:
    #     unique_together = [['name']]
# Create your models here.

class Orders(models.Model):
    orderID = models.CharField('orderID',blank=True, max_length=255,null=True)
    email = models.CharField('email',blank=True,max_length=255,null=True)
    company_name = models.CharField('company',blank=True,max_length=255,null=True)
    keyword = models.CharField(blank=True, max_length=255, null=True)
    city = models.CharField(blank=True, max_length=255, null=True)
    client_name= models.CharField(blank=True, max_length=255, null=True)
    amount = models.CharField(blank=True,max_length=255,null=True)
    net_price = models.CharField(blank=True,max_length=255,null=True)
    status = models.CharField(blank=True,max_length=255,null=True)
    address = models.CharField(blank=True,max_length=555,null=True)
    total = models.IntegerField(blank=True,null=True)

    orderDate = models.DateField(default=timezone.now())

