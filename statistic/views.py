from datetime import datetime
from rest_framework import viewsets,permissions,response,status
from rest_framework.response import Response
from statistic.tasks import save_state
from statistic.utils import  get_product_state
from . import models,serializers


class ProductView(viewsets.ModelViewSet):
    """ CRUD карточек товара"""
    serializer_class = serializers.ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return models.ProductCard.objects.filter(user = self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def create(self, request):
        data = get_product_state(request.data.get('code'))
        if data is None:
            return Response({'Not Found':'Не удалось получить информацию о товаре'},status=status.HTTP_404_NOT_FOUND)
        
        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception = True)
        serializer.save()
        return Response({'Success':'Товар успешно создан'},status = status.HTTP_201_CREATED)


class ProductStateView(viewsets.ModelViewSet):
    """ CRUD карточек состояния товара
    """
    serializer_class = serializers.ProductStateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return models.ProductCardState.objects.all()
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    def create(self, request):
        code_id = request.data.get('card')
        product = models.ProductCard.objects.filter(pk = code_id).first()
        if not product:
            return Response({"Bad Request":'Продукт не найден'},status = status.HTTP_404_NOT_FOUND )
        
        data = save_state(product.code,product.id)
        return response.Response({"Success":data},status = status.HTTP_201_CREATED)


class TrackingView(viewsets.ModelViewSet):
    """ CRUD отслеживаний товара
    """
    serializer_class = serializers.CardTrackingSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return models.CardTracking.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self,request):
        if datetime.strptime(request.data.get('end_tracking'),'%Y-%m-%d %H:%M:%S') < datetime.today():
            return Response({'Bad Request': 'Неправильная дата конца отслеживания'},status=status.HTTP_400_BAD_REQUEST)
        return super().create(request)
        





