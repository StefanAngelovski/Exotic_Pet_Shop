from django.db import models


# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)

    def __str__(self):
        return self.name


class Animal(models.Model):
    SEX_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
    ]

    common_name = models.CharField(max_length=200)
    scientific_name = models.CharField(max_length=200)
    image = models.ImageField(upload_to='animals/')
    price = models.DecimalField(max_digits=6, decimal_places=2)
    age = models.PositiveIntegerField()
    sex = models.CharField(max_length=1, choices=SEX_CHOICES)
    traits = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.common_name
