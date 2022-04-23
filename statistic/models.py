from django.db import models
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from statistic.utils import create_task, get_product_state
from users.models import User
from django_celery_beat.models import PeriodicTask


class ProductCard(models.Model):
    """ Модель карточки товара
    """
    code = models.IntegerField(unique=True,verbose_name=_("Артикул"))
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='product')

    def __str__(self):
        return f'Продукт артикул №{self.code}'

    def clean(self) -> None:
        """ Проверка артикула на возможность получения информации
        """
        data = get_product_state(self.code)
        if not data:
            raise ValidationError(_('Не удалось получить информацию о товаре.'))
        return super().clean()


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
    card = models.ForeignKey(ProductCard,unique=True, on_delete=models.CASCADE,related_name='tracking_card')
    start_tracking = models.DateTimeField(null=False, blank=False)
    end_tracking = models.DateTimeField(null=False, blank=False)
    interval = models.PositiveIntegerField(null=False, blank=False,choices=CHOICES)
    is_active = models.BooleanField(default=True)

    def __str__(self) -> str:
        return f'{self.card}'

    def save(self,*args,**kwargs):
        """ При создании отслеживания создается задача,
            при изменении активности отслеживания соотвсетсвенно 
            меняется активность задачи
        """
        task = PeriodicTask.objects.filter(name__startswith = str(self.card.code))

        if not task.exists() and self.is_active == True: 
            create_task(self)
        elif task.exists():
            task.update(enabled = self.is_active)

        super().save(*args, **kwargs)
    
    def delete(self,*args,**kwargs):
        task = PeriodicTask.objects.filter(name__startswith = str(self.card.code))
        task.delete()
        super().delete(*args,**kwargs)

    