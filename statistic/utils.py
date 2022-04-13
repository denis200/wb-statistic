

import json
from bs4 import BeautifulSoup
import requests


def get_product_state(code):
    url = f'https://www.wildberries.ru/catalog/{code}/detail.aspx'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    brand,title = soup.find('h1',class_='same-part-kt__header').text.split('/')
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

    return product_state
