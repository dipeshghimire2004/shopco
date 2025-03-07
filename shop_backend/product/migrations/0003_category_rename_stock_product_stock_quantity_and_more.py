# Generated by Django 5.1.3 on 2024-11-23 08:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0002_remove_productimage_uniques_main_image_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.RenameField(
            model_name='product',
            old_name='stock',
            new_name='stock_quantity',
        ),
        migrations.AddField(
            model_name='product',
            name='type',
            field=models.CharField(choices=[('Tshirt', 'Tshirt'), ('Pant', 'Pant'), ('Hoodie', 'Hoodie'), ('Shirts', 'Shirts'), ('Shorts', 'Shorts')], max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='products', to='product.category'),
        ),
    ]
