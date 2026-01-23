from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Author
from .forms import NewsSearchForm , PostForm
from django.urls import reverse_lazy



class NewsListView(ListView):
    model = Post
    template_name = 'flatpages/news_list.html'  # Шаблон для списка новостей
    context_object_name = 'news_list'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(type=Post.NEWS).order_by('-created_at')

class NewsDetailView(DetailView):
    model = Post
    template_name = 'flatpages/news_detail.html'  # Шаблон для детальной страницы
    context_object_name = 'news_item'

class NewsSearchView(ListView):
    model = Post
    template_name = 'news_search.html'
    context_object_name = 'news_list'
    paginate_by = 10

    def get_queryset(self):
        queryset = Post.objects.filter(type=Post.NEWS).order_by('-created_at')
        form = self.get_form()
        if form.is_valid():
            title = form.cleaned_data.get('title')
            author = form.cleaned_data.get('author')
            created_after = form.cleaned_data.get('created_after')

            if title and title.strip():
                queryset = queryset.filter(title__icontains=title.strip())
            if author and author.strip():
                queryset = queryset.filter(author__user__username__icontains=author.strip())
            if created_after:
                queryset = queryset.filter(created_at__date__gt=created_after)  # gt, не gte
        return queryset
    def get_form(self):
        return NewsSearchForm(self.request.GET)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context


from django.views.generic import CreateView
from django.urls import reverse_lazy
from .models import Post, Author
from .forms import PostForm


class NewsCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = Post.NEWS
        if self.request.user.is_authenticated:
            author, _ = Author.objects.get_or_create(user=self.request.user)
            post.author = author
        return super().form_valid(form)

class NewsUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'
    success_url = reverse_lazy('news_list')

class NewsDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')


class ArticleCreateView(CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        post = form.save(commit=False)
        post.type = Post.ARTICLE
        if self.request.user.is_authenticated:
            author, _ = Author.objects.get_or_create(user=self.request.user)
            post.author = author
        post.save()
        return super().form_valid(form)

class ArticleUpdateView(UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'
    success_url = reverse_lazy('news_list')

class ArticleDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')




    