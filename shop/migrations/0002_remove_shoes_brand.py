# Generated by Django 4.0.5 on 2022-06-18 10:33

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shoes',
            name='brand',
        ),
    ]