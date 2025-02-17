# Generated by Django 5.0.6 on 2024-05-30 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0006_alter_group_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='group',
            options={'ordering': ['-date_added', 'title'], 'permissions': [('invite_user_group', 'Can invite user to a group'), ('remove_user_group', 'Can remove user from a group'), ('add_shop_group', 'Can add shop to a group'), ('remove_shop_group', 'Can remove shop from a group')], 'verbose_name': 'group', 'verbose_name_plural': 'groups'},
        ),
    ]
