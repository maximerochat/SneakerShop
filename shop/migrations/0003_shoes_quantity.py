# Generated by Django 4.0.5 on 2022-06-23 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_remove_shoes_brand'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoes',
            name='quantity',
            field=models.IntegerField(default=1),
        ),
    ]