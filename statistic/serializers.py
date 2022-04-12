from asyncore import read
from . import models
from rest_framework import serializers

class BaseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)


class ProductStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductCardState
        fields = ('product_name','current_price','old_price','brand_name','supplier','tracked_at')


class ProductSerializer(serializers.ModelSerializer):
    states = ProductStateSerializer(source='productcardstate_set',many=True,read_only=True)
    class Meta:
        model = models.ProductCard
        fields = ('code','user','states')