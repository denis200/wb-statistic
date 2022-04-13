import datetime
from random import choices
from django.db import models
from django.utils.translation import gettext_lazy as _

from users.models import User


class ProductCard(models.Model):
    """ Модель карточки товара
    """
    code = models.IntegerField(unique=True,verbose_name=_("Артикул"))
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='product')

    def __str__(self):
        return f'Продукт артикул №{self.code}'


class ProductCardState(models.Model):
    """ Модель состояния карточки товара
    """
    code = models.ForeignKey(ProductCard,verbose_name=_("Артикул"),on_delete=models.DO_NOTHING)
    product_name = models.CharField(max_length=255,verbose_name=_("Название продукта"))
    current_price = models.PositiveIntegerField(verbose_name=_("Текущая цена"))
    old_price = models.PositiveIntegerField(verbose_name=_("Старая цена"),null=True,blank = True)
    brand_name = models.CharField(max_length=150,verbose_name=_("Название бренда"))
    supplier = models.CharField(max_length=150,verbose_name=_("Поставщик"))
    tracked_at = models.DateTimeField(auto_now_add=True)


class CardTracking(models.Model):
    """ Модель отслеживания карточки товара
    """
    CHOICES = [
        (1,  '1 hour'),
        (12, '12 hours'),
        (24,'24 hours'),
    ]

    user = models.ForeignKey(User,on_delete=models.CASCADE)
    card = models.ForeignKey(ProductCard,on_delete=models.CASCADE,related_name='tracking_card')
    start_tracking = models.DateTimeField(null=False, blank=False)
    end_tracking = models.DateTimeField(null=False, blank=False)
    interval = models.PositiveIntegerField(null=False, blank=False,choices=CHOICES)
    is_active = models.BooleanField(default=True)