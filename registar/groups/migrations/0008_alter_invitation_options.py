# Generated by Django 5.0.6 on 2024-05-30 20:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('groups', '0007_alter_group_options'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='invitation',
            options={'permissions': [('accept_invitation', 'Can accept invitation'), ('reject_invitation', 'Can reject invitation')], 'verbose_name': 'invitation', 'verbose_name_plural': 'invitations'},
        ),
    ]
