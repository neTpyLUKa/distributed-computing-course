# Generated by Django 3.0.7 on 2020-06-13 05:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.IntegerField(choices=[(0, 'User'), (1, 'Admin')], default=1),
        ),
    ]
