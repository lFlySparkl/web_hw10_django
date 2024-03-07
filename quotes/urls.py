# from django.contrib import admin
from django.urls import path
from . import views
from .views import author_detail, tag_detail, top_tags

app_name = "quotes"

urlpatterns = [
    path("", views.main, name="main"),
    path("<int:page>", views.main, name="root_paginate"),
    path('tag/<str:tag_name>/', tag_detail, name='tag_detail'),
    path('tag/<str:tag_name>/<int:page>/', tag_detail, name='tag_detail_paginated'),
    path('author/<str:author_name>/', author_detail, name='author_detail'),
    path('add_author/', views.add_author, name='add_author'),
    path('add_quote/', views.add_quote, name='add_quote'),
    path('top_tags/', top_tags, name='top_tags'),
]
