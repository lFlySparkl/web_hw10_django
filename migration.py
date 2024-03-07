import os
import django
from pymongo import MongoClient

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_hw10_django.settings")
django.setup()

from quotes.models import Quote, Tag, Author  # noqa

client = MongoClient("mongodb://localhost:27017")
db = client.my_mongodb

authors = db.author.find()

for author in authors:
    defaults = {
        'born_date': author['born_date'],
        'born_location': author['born_location'],
        'description': author['description'],
    }
    try:
        author_obj, created = Author.objects.get_or_create(
            fullname=author['fullname'],
            born_date=author['born_date'],
            defaults=defaults
        )
        print(f"Author: {author_obj.fullname}, Created: {created}")
    except Author.MultipleObjectsReturned:
        print(f"Multiple authors found for: {author['fullname']}")

quotes = db.quote.find()

for quote in quotes:
    print(f"Reading quote from MongoDB: {quote}")
    tags = []
    for tag in quote['tags']:
        t, created = Tag.objects.get_or_create(name=tag)
        tags.append(t)
        print(f"Tag: {t.name}, Created: {created}")

    existing_quotes = Quote.objects.filter(quote=quote['quote'])

    if not existing_quotes.exists():
        print(quote['author'])
        author = db.author.find_one({'_id': quote['author']})

        if author:
            authors = Author.objects.filter(fullname=author['fullname'])

            if authors.exists():
                a = authors.first()  # Или другим способом выбрать нужный объект
                created = False
            else:
                a = Author.objects.create(fullname=author['fullname'])
                created = True
            print(f"Attempting to create Quote for: {quote['quote']}")
            q = Quote.objects.create(quote=quote['quote'], author=a)

            for tag in tags:
                q.tags.add(tag)
            print(f"Quote added to PostgreSQL: {q}")
            print(f"Author: {a.fullname}, Created: {created}")
        else:
            print(f"Author not found in MongoDB for quote: {quote['quote']}")
    else:
        print(f"Quote already exists in PostgreSQL: {existing_quotes.first()}")
