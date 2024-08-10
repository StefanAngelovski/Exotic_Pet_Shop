from django.db import models
from django.contrib.auth.models import User
from django.db.models import OneToOneField
from django_ckeditor_5.fields import CKEditor5Field


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Animal(models.Model):
    common_name = models.CharField(max_length=200, null=True, blank=True)
    scientific_name = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='animals/', null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    description = CKEditor5Field('Description', null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.common_name


class SupplyCategory(models.Model):
    name = models.CharField(max_length=200)
    icon = models.ImageField(upload_to='supply_categories/', null=True, blank=True)

    def __str__(self):
        return self.name


class Supplies(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image = models.ImageField(upload_to='supplies/', null=True, blank=True)
    supply_category = models.ForeignKey(SupplyCategory, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    total_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self):
        return self.user.username + "'s cart"


class CartItem(models.Model):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items', null=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, null=True, blank=True)
    supply = models.ForeignKey(Supplies, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    age = models.PositiveIntegerField(null=True, blank=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.animal.common_name if self.animal else self.supply.name

    @property
    def total_price(self):
        return self.animal.price * self.quantity if self.animal else self.supply.price * self.quantity


class UserProfile(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20, null=True, blank=True)
    shipping_name = models.CharField(max_length=200, null=True, blank=True)
    shipping_address = models.TextField(null=True, blank=True)
    shipping_city = models.CharField(max_length=200, null=True, blank=True)
    shipping_state = models.CharField(max_length=200, null=True, blank=True)
    shipping_zip = models.CharField(max_length=200, null=True, blank=True)
    cart = models.OneToOneField(Cart, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.user.username
