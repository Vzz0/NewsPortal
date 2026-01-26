from django.contrib import admin
from django.urls import path, include
from news.views import PostDeleteView, PostUpdateView, PostCreateView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('news/', include('news.urls')),

#Статьи
    path('articles/create/', PostCreateView.as_view(),{'post_type': 'article'}, name='article_create'),
    path('articles/<int:pk>/update/', PostUpdateView.as_view(), name='article_edit'),
    path('articles/<int:pk>/delete/', PostDeleteView.as_view(), name='article_delete'),
    path('accounts/', include('allauth.urls')),
]