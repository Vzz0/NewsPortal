from django.contrib import admin
from django.urls import path, include
from news.views import (
    ArticleCreateView,
    ArticleUpdateView,
    ArticleDeleteView
)
urlpatterns = [
    path('admin/', admin.site.urls),
    path('news/', include('news.urls')),

#Статьи
    path('articles/create/', ArticleCreateView.as_view(), name='article_create'),
    path('articles/<int:pk>/update/', ArticleUpdateView.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', ArticleDeleteView.as_view(), name='article_delete'),
]