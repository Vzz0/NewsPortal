from django.urls import path
from .views import NewsListView, NewsDetailView, NewsSearchView, PostDeleteView, PostUpdateView, PostCreateView
from . import views
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', cache_page(60)(NewsListView.as_view()), name='news_list'),
    path('<int:pk>/',cache_page(60* 5)(NewsDetailView.as_view()), name='news_detail'),
    path('create/', PostCreateView.as_view(), name='news_create'),
    path('search/', NewsSearchView.as_view(), name='news_search'),
    path('<int:pk>/update/', PostUpdateView.as_view(), name='news_edit'),
    path('<int:pk>/delete/', PostDeleteView.as_view(), name='news_delete'),
    path('profile/', views.user_profile, name='user_profile'),
    path('profile/upgrade/', views.upgrade_to_author, name='upgrade_to_author'),
    path('subscribe/<int:category_id>/', views.subscribe, name='subscribe'),
    ]