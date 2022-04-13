from django.shortcuts import render
from rest_framework import viewsets,permissions,views,response

from statistic.utils import get_product_state
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


class GetProductState(views.APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self,request):
        code = request.data.get('code')
        product = models.ProductCard.objects.filter(code = code).first()
        if not product:
            product = models.ProductCard.objects.create(code = code,user=self.request.user)
            product.save()
        state = get_product_state(code)
        state['code'] = product.id
        serializer = serializers.ProductStateSerializer(data = state)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return response.Response({"success":serializer.data})



