from django.db import models
from django.db.models import F
from django.db.models import Sum


class Author(models.Model):
    fullname = models.CharField(max_length=50)
    born_date = models.CharField(max_length=50)
    born_location = models.CharField(max_length=150)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.fullname


class Tag(models.Model):
    name = models.CharField(max_length=50, null=False, unique=True)
    popularity = models.IntegerField(default=0)

    def __str__(self):
        return self.name

    @classmethod
    def update_popularity(cls):
        # Обновляем популярность тегов
        tags_with_popularity = cls.objects.annotate(tag_popularity=Sum('quote__popularity'))
        for tag in tags_with_popularity:
            cls.objects.filter(id=tag.id).update(popularity=F('tag_popularity'))

class Quote(models.Model):

    quote = models.TextField()
    tags = models.ManyToManyField(Tag)
    author = models.ForeignKey(
        Author, on_delete=models.CASCADE, default=None, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
