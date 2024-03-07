from django import template
from quotes.models import Tag, Author, Quote

register = template.Library()

@register.filter(name='author')
def get_author(id_):
    try:
        author = Author.objects.get(id=id_)
        return author.fullname
    except Author.DoesNotExist:
        return None

@register.filter(name='tag_quote')
def tag_quote(id_):
    try:
        tag = Tag.objects.get(id=id_)
        quotes = Quote.objects.filter(tags=tag)
        return quotes
    except Tag.DoesNotExist:
        return None