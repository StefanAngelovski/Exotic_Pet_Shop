# Generated by Django 5.0.6 on 2024-08-09 08:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0002_remove_animal_new_description_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupplyCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Supplies',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.TextField(blank=True, null=True)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='supplies/')),
                ('supply_category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='Store.supplycategory')),
            ],
        ),
    ]
