from django.db import models

from django.utils.translation import gettext_lazy as _

from users.models import User


class Product(models.Model):
    user_id = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='user_products',
        verbose_name=_('Пользователь')
    )
    title = models.CharField(max_length=100, verbose_name=_('Наименование'))
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name=_('Цена'))
    short_description = models.TextField(verbose_name=_('Короткое описание'))
    long_description = models.TextField(verbose_name=_('Длинное описание'))
    likes_count = models.IntegerField(default=0, verbose_name=_('Количество лайков'))

    # Главное изображение
    product_image = models.ImageField(
        null=True, blank=True, upload_to='products/%Y/%m/%d', verbose_name='Изображение товара'
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('Товар')
        verbose_name_plural = _('Товары')


class ProductImage(models.Model):
    product_id = models.ForeignKey(
        to=Product,
        on_delete=models.CASCADE,
        related_name='product_images',
        verbose_name=_('Товар')
    )
    image = models.ImageField(upload_to='products_images/%Y/%m/%d', verbose_name=_('Изображение'))
    likes_count = models.IntegerField(default=0, verbose_name=_('Количество лайков'))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = _('Изображение товара')
        verbose_name_plural = _('Изображения товара')


class FavoriteProduct(models.Model):
    user_id = models.ForeignKey(
        to=User,
        on_delete=models.CASCADE,
        related_name='user_favorites',
        verbose_name=_('Пользователь')
    )
    product_id = models.OneToOneField(
        to=Product,
        on_delete=models.CASCADE,
        related_name='product_favorites',
        verbose_name=_('Товар')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)
        verbose_name = _('Понравившийся товар')
        verbose_name_plural = _('Понравившиеся товары')
