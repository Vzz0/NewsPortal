from django.urls import path
from .views import NewsListView, NewsDetailView, NewsSearchView, NewsUpdateView, NewsDeleteView, NewsCreateView

urlpatterns = [
    #Новости
    path('', NewsListView.as_view(), name='news_list'),
    path('<int:pk>/', NewsDetailView.as_view(), name='news_detail'),
    path('create/', NewsCreateView.as_view(), name='news_create'),
    path('search/', NewsSearchView.as_view(), name='news_search'),
    path('<int:pk>/update/', NewsUpdateView.as_view(), name='news_edit'),
    path('<int:pk>/delete/', NewsDeleteView.as_view(), name='news_delete'),
    ]