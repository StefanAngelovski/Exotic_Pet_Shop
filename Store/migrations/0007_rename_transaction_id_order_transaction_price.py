# Generated by Django 5.0.6 on 2024-08-19 10:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Store', '0006_alter_category_options_alter_supplies_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='transaction_id',
            new_name='transaction_price',
        ),
    ]
