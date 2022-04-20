from django.shortcuts import render
from rest_framework import viewsets,permissions,views,response,generics
from .tasks import get_state_task,print_hello
from statistic.utils import get_product_state
from . import models,serializers,tasks
from django_celery_beat.models import PeriodicTask,IntervalSchedule
import json
from datetime import datetime, timedelta

from django.utils import timezone

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
        #заменить на get_or_create
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


class PrintView(views.APIView):
    def get(self,request):
        schedule = IntervalSchedule.objects.create(every=10, period=IntervalSchedule.HOURS)
        PeriodicTask.objects.create(
          name='First',
          task='print_hello',
          interval = schedule,
          start_time=timezone.now(),
        )
        return response.Response({'ura':'ura'})


class TrackingView(generics.CreateAPIView):
    queryset = models.CardTracking.objects.all()
    serializer_class = serializers.CardTrackingSerializer

    def perform_create(self,serializer_class):
        schedule = IntervalSchedule.objects.create(every=10, period=IntervalSchedule.SECONDS)
        PeriodicTask.objects.create(
          name=f'Get Product State {datetime.now()}',
          task='statistic.tasks.get_state_task',
          interval = schedule,
          start_time=timezone.now(),
          args = json.dumps(['8888430']),
          expires = timezone.now() + timedelta(seconds=30),
        )





