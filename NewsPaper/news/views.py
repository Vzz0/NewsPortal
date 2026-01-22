from django.views.generic import ListView, DetailView
from .models import Post

class NewsListView(ListView):
    model = Post
    template_name = 'flatpages/news_list.html'  # Шаблон для списка новостей
    context_object_name = 'news_list'
    paginate_by = 5

    def get_queryset(self):
        return Post.objects.filter(type=Post.NEWS).order_by('-created_at')

class NewsDetailView(DetailView):
    model = Post
    template_name = 'flatpages/news_detail.html'  # Шаблон для детальной страницы
    context_object_name = 'news_item'
    