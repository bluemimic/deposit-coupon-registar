# Generated by Django 5.0.6 on 2024-06-05 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_remove_coupon_coupon_uuid_alter_coupon_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='is_on_marketplace',
            field=models.BooleanField(default=False, verbose_name='is shop on marketplace?'),
        ),
    ]
