# Generated by Django 4.0.5 on 2022-06-18 10:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Nike',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300)),
            ],
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('option', models.CharField(max_length=300)),
                ('id_brand', models.AutoField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Shoes',
            fields=[
                ('description', models.TextField()),
                ('title', models.CharField(max_length=200)),
                ('price', models.IntegerField()),
                ('auto_increment_id', models.AutoField(primary_key=True, serialize=False)),
                ('size', models.FloatField(default=40.0)),
                ('brand', models.CharField(blank=True, choices=[('Nike', 'Nike'), ('Adidas', 'Adidas')], max_length=300)),
                ('id_brand', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='shop.option')),
            ],
        ),
        migrations.CreateModel(
            name='Images',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(upload_to='images/')),
                ('img_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shop.shoes')),
            ],
        ),
    ]
