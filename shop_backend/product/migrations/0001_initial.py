# Generated by Django 5.1.3 on 2024-11-22 02:17

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Size',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('category', models.CharField(choices=[('Tshirt', 'Tshirt'), ('Pant', 'Pant'), ('Hoodie', 'Hoodie'), ('Shirts', 'Shirts'), ('Shorts', 'Shorts')], max_length=20, null=True)),
                ('style', models.CharField(choices=[('Casual', 'Casual'), ('Formal', 'Formal'), ('Party', 'Party'), ('Gym', 'Gym')], max_length=20, null=True)),
                ('rate', models.DecimalField(decimal_places=2, max_digits=10)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('discount', models.DecimalField(decimal_places=2, max_digits=4)),
                ('discounted_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('description', models.TextField(blank=True, max_length=300)),
                ('main_image', models.ImageField(blank=True, null=True, upload_to='main_images/')),
                ('stock', models.PositiveIntegerField()),
                ('colors', models.ManyToManyField(to='product.color')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='products', to=settings.AUTH_USER_MODEL)),
                ('sizes', models.ManyToManyField(to='product.size')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='product_images/')),
                ('is_main_image', models.BooleanField(default=False)),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='product.product')),
            ],
            options={
                'constraints': [models.UniqueConstraint(condition=models.Q(('is_main_image', True)), fields=('product', 'is_main_image'), name='uniques_main_image')],
            },
        ),
    ]