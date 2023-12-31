# Generated by Django 4.1.7 on 2023-07-03 16:16

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_product_likes_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='productimage',
            name='likes_count',
            field=models.IntegerField(default=0, verbose_name='Количество лайков'),
        ),
        migrations.AlterField(
            model_name='favoriteproduct',
            name='product_id',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='product_favorites', to='products.product', verbose_name='Товар'),
        ),
    ]
