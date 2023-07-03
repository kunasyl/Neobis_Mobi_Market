from django.contrib import admin

from .models import User, Profile, PhoneVerification
from products.models import FavoriteProduct


class FavoritesInline(admin.TabularInline):
    model = FavoriteProduct
    extra = 1


class ProfileInline(admin.TabularInline):
    model = Profile
    extra = 1


class UserAdmin(admin.ModelAdmin):
    inlines = (ProfileInline, FavoritesInline)


admin.site.register(Profile)
admin.site.register(FavoriteProduct)
admin.site.register(PhoneVerification)
admin.site.register(User, UserAdmin)
