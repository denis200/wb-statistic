# wb-statistic
## Стек проекта
Проект написан на Django Rest Framework + PostgreSQL + Celery + Docker

## Описание проекта
Приложение для отслеживания состояния продукта на маркетплейсе WildBerries.
Пользователь добавляет артикул товара, далее добавляет отслеживание,задавая промежуток времени,в котором нужно получать данные о товаре, 
и интервал - с какой периодичностью это делать в заданном промежутке.Приложение работает хорошо как через admin panel так и через запросы.
Запросы о состоянии товара происходят асинхронно с помощью Celery.
Подробнее в файле "Тестовое задание",который расположен в корне проета.

## Installation

Для начала переименуйте  ".env.example"  - > ".env" 

После создайте базу данных postgres и в данный файл введите соответствующие поля.
```
POSTGRES_USER=#db credentials
POSTGRES_PASSWORD=#db credentials
```
Чтобы поднять контейнер, выполните команду:
```
docker-compose up --build
```

Для того чтобы создать суперпользователя выполните команду и введите данные:

```
docker-compose exec web python manage.py createsuperuser
```

## API endpoints
### Users

POST [/api/v1/auth/users/]() - Регистрация пользователя
```
{
    "username": "",
    "email": "",
    "password": ""
}
```
POST [/api/v1/auth/jwt/create/]() - Авторизация
```
{
    "email":"",
    "password":""
}
```
### Карточка товара(ProductCard)

 GET [api/v1/statistic/productcard]() - Получить список карточек пользователя\
 POST [api/v1/statistic/productcard]() - Добавить каточку товара
```
{
    "code":"Артикул товара"
}
```

PUT [api/v1/statistic/productcard/<int:pk>]() - Обновить информацию о карточке\
DELETE [api/v1/statistic/productcard/<int:pk>]() - Удалить карточку товара

### Состояние карточки( ProductCardState)

 GET [api/v1/statistic/productstate]() - Получить список состояний пользователя\
 POST [api/v1/statistic/productstate]() - Добавить состояние
```
{
  "product_name": "Название товара",
  "current_price": Текущая цена,
  "old_price": Старая цена,
  "brand_name": "Название бренда",
  "supplier": "Поставщик",
  "code": id карточки товара
    }
```

PUT [api/v1/statistic/productstate/<int:pk>]() - Обновить информацию о состоянии карточки\
DELETE [api/v1/statistic/productstate/<int:pk>]() - Удалить состояние карточки

### Отслеживание товара (TrackingCard)

 GET [api/v1/statistic/cardtracking]() - Получение списка текущих отслеживаний\
 POST [api/v1/statistic/cardtracking]() - Добавить отслеживание
```
{   
    "start_tracking": "Дата начала отслеживания в формате yyyy-mm-dd hh:mm:ss", 
    "end_tracking": "Дата конца отслеживания в формате yyyy-mm-dd hh:mm:ss",
    "interval": Интервал отслеживания (1,12 или 24),в часах,
    "user":id пользователя,
    "card":id карточки товара,
    "is_active": true/false - активно или нет ваше остлеживание.
}
```

PUT [api/v1/statistic/productstate/<int:pk>]() - Обновить информацию об отслеживании\
DELETE [api/v1/statistic/productstate/<int:pk>]() - Удалить отслеживание.

## Немного о работе приложения
При создании карточки товара идет автоматическая проверка на то, удалось ли получить по нему информацию.Некоректную карточку сохранить нельзя.
После добавлении карточки, мы можем добавить ее отслеживание.При создании ослеживания создается celery таск который по заданным параметрам определяет 
расписание, по которому он будет получать информацию. В отслеживании есть переменная is_active при изменении которой отслеживание можно поставить на паузу.
В настоящий момент времени для удобства тестировки часы заменены на секунды.Чтобы сделать рабочий вариант программы для этого в каталоге statistic/utils в функции create_task()
в строке 
```
schedule,_ = IntervalSchedule.objects.get_or_create(every=data.interval, period=IntervalSchedule.SECONDS)
```

Нужно заменить IntervalSchedule.SECONDS на IntervalSchedule.HOURS, чтобы получилось:

```
schedule,_ = IntervalSchedule.objects.get_or_create(every=data.interval, period=IntervalSchedule.HOURS)
```
### PS. Приложение удобнее использовать через admin panel : - )
