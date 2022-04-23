from statistic import models
from rest_framework import serializers


class BaseSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)


class ProductStateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ProductCardState
        fields = ('__all__')


class ProductSerializer(BaseSerializer, serializers.ModelSerializer):
    states = ProductStateSerializer(source='productcardstate_set',many=True,read_only=True)
    class Meta:
        model = models.ProductCard
        fields = ('id','code','user','states')


class CardTrackingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CardTracking
        fields = ('__all__')