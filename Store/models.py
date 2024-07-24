from django.db import models
from django.contrib.auth.models import User
from django.db.models import OneToOneField
from ckeditor.fields import RichTextField


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
    description = RichTextField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.common_name


class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    total_price = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    cart_items = models.ManyToManyField('CartItem')

    def __str__(self):
        return self.user.username + "'s cart"


class CartItem(models.Model):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]
    age = models.PositiveIntegerField(null=True, blank=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, null=True, blank=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.animal.common_name


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
