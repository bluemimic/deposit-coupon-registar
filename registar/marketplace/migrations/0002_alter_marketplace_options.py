# Generated by Django 5.0.6 on 2024-06-05 10:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marketplace', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='marketplace',
            options={'default_permissions': (), 'managed': False, 'permissions': (('view_', 'Can view a shop on the marketplace'),)},
        ),
    ]