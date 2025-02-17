# Generated by Django 5.0.6 on 2024-05-26 10:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_rename_user_coupon_owner'),
        ('groups', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='groupmembership',
            options={'verbose_name': 'group membership', 'verbose_name_plural': 'group memberships'},
        ),
        migrations.AlterModelOptions(
            name='shopgroup',
            options={'verbose_name': 'shop group', 'verbose_name_plural': 'shop groups'},
        ),
        migrations.AddConstraint(
            model_name='groupmembership',
            constraint=models.UniqueConstraint(fields=('user', 'group'), name='unique_group_membership'),
        ),
        migrations.AddConstraint(
            model_name='shopgroup',
            constraint=models.UniqueConstraint(fields=('shop', 'group'), name='unique_shop_group'),
        ),
    ]
