from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Quote, Author, Tag
from .forms import AuthorForm, QuoteForm
from django.db.models import F

# Create your views here.
def main(request, page=1):
    per_page = 10
    quotes = Quote.objects.all()
    paginator = Paginator(quotes, per_page)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes/index.html', context={'quotes': quotes_on_page})

def author_detail(request, author_name):
    authors = Author.objects.filter(fullname=author_name)
    
    if not authors.exists():
        # Обработка случая, когда автор не найден
        return render(request, 'quotes/author_not_found.html', {'author_name': author_name})
    
    author = authors.first()

    return render(request, 'quotes/author_detail.html', {'author': author})

def tag_detail(request, tag_name):
    quotes_list = Quote.objects.filter(tags__name=tag_name)
    paginator = Paginator(quotes_list, 10)
    
    page = request.GET.get('page')
    quotes = paginator.get_page(page)
    
    context = {'tag': tag_name, 'quotes': quotes}
    return render(request, 'quotes/tag_detail.html', context)

def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save()
            return redirect('quotes:author_detail', author_name=author.fullname)
    else:
        form = AuthorForm()

    return render(request, 'quotes/add_author.html', {'form': form})

def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('quotes:main')
    else:
        form = QuoteForm()

    all_tags = Tag.objects.all()
    all_authors = Author.objects.all()

    return render(request, 'quotes/add_quote.html', {'form': form, 'all_tags': all_tags, 'all_authors': all_authors})


def top_tags(request):
    # Обновляем популярность тегов
    update_tags_popularity()

    # Получаем 10 самых популярных тегов
    top_tags = Tag.objects.order_by('-popularity')[:10]

    # Возвращаем шаблон с данными
    return render(request, 'quotes/top_tags.html', {'top_tags': top_tags})

def update_tags_popularity():
    # Очищаем популярность у всех тегов перед обновлением
    Tag.objects.all().update(popularity=0)

    # Обновляем популярность тегов на основе цитат
    for quote in Quote.objects.all():
        for tag in quote.tags.all():
            Tag.objects.filter(name=tag.name).update(popularity=F('popularity') + 1)