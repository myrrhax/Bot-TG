from django.contrib import admin
from .models import Items, User, Purchase, Referral


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'name', 'scores')


@admin.register(Items)
class ItemsAdmin(admin.ModelAdmin):
    list_display = ('item_id', 'name', 'price')


@admin.register(Referral)
class ReferralAdmin(admin.ModelAdmin):
    list_display = ('id', 'referrer_id', 'referral_id')


@admin.register(Purchase)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_id', 'item_id', 'price',
                    'quantity', 'phone_number',
                    'shipping_address', 'status')

