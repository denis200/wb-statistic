from celery import shared_task
from config.celery import app
from . import serializers
from statistic.utils import get_product_state


@app.task
def get_state_task(code):
    data = get_product_state(code)
    data['code'] = 1
    print(type(data))
    ser = serializers.ProductStateSerializer(data = data)
    ser.is_valid(raise_exception=True)
    ser.save()
    return ser.data


@app.task
def print_hello():
    print('hello world')
    return 2