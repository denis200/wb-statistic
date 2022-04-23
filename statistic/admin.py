from django.contrib import admin
from .models import CardTracking, ProductCard, ProductCardState


@admin.register(ProductCard)
class ProductAdmin(admin.ModelAdmin):
    list_display =('id','code',)


@admin.register(ProductCardState)
class ProductCardStateAdmin(admin.ModelAdmin):
    list_display = ('code','product_name','current_price','old_price','brand_name','supplier','tracked_at')
    list_display_links = ('code','product_name','current_price','old_price','brand_name','supplier','tracked_at')


@admin.register(CardTracking)
class CardTrackingAdmin(admin.ModelAdmin):
    list_display = ('user','card','start_tracking','end_tracking','interval')
    list_display_links = ('user','card','start_tracking','end_tracking','interval')
    