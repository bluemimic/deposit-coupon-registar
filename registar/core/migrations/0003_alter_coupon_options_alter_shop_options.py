# Generated by Django 5.0.6 on 2024-05-21 16:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_coupon_barcode_alter_coupon_title_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='coupon',
            options={'ordering': ['-date_added', 'title'], 'verbose_name': 'coupon', 'verbose_name_plural': 'coupons'},
        ),
        migrations.AlterModelOptions(
            name='shop',
            options={'ordering': ['-date_added', 'title'], 'verbose_name': 'shop', 'verbose_name_plural': 'shops'},
        ),
    ]