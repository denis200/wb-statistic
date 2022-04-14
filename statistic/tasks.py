from celery import shared_task
from config.celery import app
from statistic.utils import get_product_state


@app.task
def get_state_task(code):
    data = get_product_state(code)
    return data


@shared_task()
def print_hello():
    print('hello')