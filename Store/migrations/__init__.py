from django.db import migrations


def forwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it will be the wrong version
    Animal = apps.get_model('Store', 'Animal')
    for animal in Animal.objects.all():
        animal.description = animal.old_description
        animal.save()


def backwards_func(apps, schema_editor):
    # We get the model from the versioned app registry;
    # if we directly import it, it will be the wrong version
    Animal = apps.get_model('Store', 'Animal')
    for animal in Animal.objects.all():
        animal.old_description = animal.description
        animal.save()


class Migration(migrations.Migration):
    dependencies = [
        ('Store', 'previous_migration'),  # replace with your previous migration
    ]

    operations = [
        migrations.RunPython(forwards_func, backwards_func),
    ]
