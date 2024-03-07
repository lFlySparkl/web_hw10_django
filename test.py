import os
import django
from django.conf import settings

# Устанавливаем переменную окружения DJANGO_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_hw10_django.settings")

# Инициализация Django
django.setup()

# Импорт моделей Django
from quotes.models import Quote

try:
    # Получение всех объектов Quote из PostgreSQL
    quotes = Quote.objects.all()

    if not quotes.exists():
        print("Нет данных в таблице Quote.")

    for quote in quotes:
        print(f"Quote: {quote.quote}, Author: {quote.author.fullname}, Tags: {[tag.name for tag in quote.tags.all()]}")

except Exception as e:
    print(f"Ошибка при получении данных из PostgreSQL: {e}")

from quotes.models import Tag

try:
    # Получение всех объектов Quote из PostgreSQL
    tags = Tag.objects.all()

    if not tags.exists():
        print("Нет данных в таблице Tags.")

    for tag in tags:
        print(f"Tag: {tag.name}")

except Exception as e:
    print(f"Ошибка при получении данных из PostgreSQL: {e}")

# from pymongo import MongoClient

# # Подключение к MongoDB
# client = MongoClient("mongodb://localhost:27017")
# db = client.my_mongodb  # Замените на имя вашей базы данных

# # Удаление коллекции (таблицы) 'author'
# db.author.drop()

# # Удаление коллекции 'quote'
# db.quote.drop()

# # Удаление коллекции 'tag'
# db.tag.drop()