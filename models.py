# models.py
from mongoengine import Document, StringField, ReferenceField, ListField

class Author(Document):
    fullname = StringField(max_length=50)
    born_date = StringField(max_length=50)
    born_location = StringField(max_length=150)
    description = StringField()
    created_at = StringField()

class Tag(Document):
    name = StringField(max_length=50, required=True, unique=True)

class Quote(Document):
    quote = StringField()
    tags = ListField(ReferenceField(Tag))
    author = ReferenceField(Author)
    created_at = StringField()