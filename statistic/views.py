from django.shortcuts import render
from rest_framework import viewsets,permissions,views,response
from . import models,serializers

class ProductView(viewsets.ModelViewSet):
    """ CRUD карточек товара"""
    serializer_class = serializers.ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return models.ProductCard.objects.filter(user = self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProductStateView(viewsets.ModelViewSet):
    """ CRUD карточек состояния товара"""
    serializer_class = serializers.ProductStateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return models.ProductCardState.objects.all()