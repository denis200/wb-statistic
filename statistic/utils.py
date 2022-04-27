import json
from bs4 import BeautifulSoup
import requests
from django_celery_beat.models import PeriodicTask,IntervalSchedule
import json
from datetime import datetime

from . import models

def get_product_state(code):
    """ Получение данных с сайта Wildberries
    """
    url = f'https://www.wildberries.ru/catalog/{code}/detail.aspx'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    try:
        brand = soup.find('h1',class_='same-part-kt__header').text.split('/')[0].replace(u'\xa0', '').strip()
        title = soup.find('h1',class_='same-part-kt__header').text.split('/')[1].replace(u'\xa0', '').strip()
        current_price = soup.find('span',class_='price-block__final-price').text.replace(u'\xa0', '').strip()[:-1]
        try:
            old_price = soup.find(class_='price-block__old-price').text.replace(u'\xa0', '')[:-1]
        except AttributeError:
            old_price = None
        seller = requests.get(f"https://wbx-content-v2.wbstatic.net/sellers/{code}.json").json()['supplierName']

        product_state = {
            "product_name" : title,
            "current_price": current_price,
            "old_price": old_price,
            "brand_name": brand,
            "supplier":seller,
        }
    except Exception as e:
        product_state = None
        
        
    return product_state


def create_task(data):
    """ Создание задачи celery
    """
    schedule,_ = IntervalSchedule.objects.get_or_create(every=data.interval, period=IntervalSchedule.SECONDS)
    code = models.ProductCard.objects.get(pk = data.card.pk).code
    PeriodicTask.objects.create(
          name=f'{code} | Get Product State | {datetime.now()}',
          task='statistic.tasks.get_state_task',
          interval = schedule,
          start_time=data.start_tracking,
          args = json.dumps([code,data.card.id]),
          expires = data.end_tracking,
        )
