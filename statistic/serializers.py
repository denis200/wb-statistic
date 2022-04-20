from asyncore import read
from . import models
from rest_framework import serializers

class BaseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)


class ProductStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductCardState
        fields = ('__all__')


class ProductSerializer(serializers.ModelSerializer):
    states = ProductStateSerializer(source='productcardstate_set',many=True,read_only=True)
    class Meta:
        model = models.ProductCard
        fields = ('code','user','states')


class CardTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CardTracking
        fields = ('__all__')