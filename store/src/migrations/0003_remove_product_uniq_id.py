# Generated by Django 3.0.4 on 2020-06-12 08:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0002_product_uniq_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='uniq_id',
        ),
    ]
