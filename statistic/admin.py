from django.contrib import admin
from .models import CardTracking, ProductCard


@admin.register(ProductCard)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ('code','product_name','current_price','old_price','brand_name','supplier')
    list_display_links = ('code','product_name','current_price','old_price','brand_name','supplier')


@admin.register(CardTracking)
class LicenseAdmin(admin.ModelAdmin):
    list_display = ('user','card','start_tracking','end_tracking','interval')
    list_display_links = ('user','card','start_tracking','end_tracking','interval')