from django.views.generic import ListView, DetailView
from .models import Post

class NewsListView(ListView):
    model = Post
    template_name = 'news/news_list.html'  # Шаблон для списка новостей
    context_object_name = 'news_list'
    paginate_by = 5  # Если нужно пагинацию

    def get_queryset(self):
        # Фильтруем только новости (тип = 'новость')
        return Post.objects.filter(type=Post.NEWS).order_by('-created_at')

class NewsDetailView(DetailView):
    model = Post
    template_name = 'news/news_detail.html'  # Шаблон для детальной страницы
    context_object_name = 'news_item'
    