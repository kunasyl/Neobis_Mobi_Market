from django.contrib import admin
from . import models


class ProductImageInline(admin.TabularInline):
    model = models.ProductImage
    extra = 1


class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'price')
    list_filter = ('user_id', )
    search_fields = ('title', )
    inlines = (ProductImageInline,)


admin.site.register(models.ProductImage)
admin.site.register(models.Product, ProductAdmin)
