# Generated by Django 4.0.5 on 2022-06-18 22:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cart',
            name='quantity',
            field=models.JSONField(default={}),
            preserve_default=False,
        ),
    ]
