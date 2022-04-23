from django.contrib import admin
from rest_framework.response import Response
from statistic.utils import get_product_state
from .models import CardTracking, ProductCard, ProductCardState
from django import forms


@admin.register(ProductCard)
class ProductAdmin(admin.ModelAdmin):
    list_display =('id','code',)

    def save_model(self, request, obj, form, change) :
        return super().save_model(request, obj, form, change)


@admin.register(ProductCardState)
class ProductCardStateAdmin(admin.ModelAdmin):
    list_display = ('code','product_name','current_price','old_price','brand_name','supplier','tracked_at')
    list_display_links = ('code','product_name','current_price','old_price','brand_name','supplier','tracked_at')


@admin.register(CardTracking)
class CardTrackingAdmin(admin.ModelAdmin):
    list_display = ('user','card','start_tracking','end_tracking','interval')
    list_display_links = ('user','card','start_tracking','end_tracking','interval')
    