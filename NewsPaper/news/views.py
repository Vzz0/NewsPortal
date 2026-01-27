from django.contrib.auth.models import Group
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.conf import settings
from .models import Post, Category, Author
from .forms import NewsSearchForm, PostForm
from django.utils import timezone

class NewsListView(ListView):
    model = Post
    template_name = 'flatpages/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(type=Post.NEWS).order_by('-created_at')


class NewsDetailView(DetailView):
    model = Post
    template_name = 'flatpages/news_detail.html'
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
                queryset = queryset.filter(created_at__date__gt=created_after)
        return queryset

    def get_form(self):
        return NewsSearchForm(self.request.GET)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context


class PostCreateView(PermissionRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'post_create.html'
    permission_required = 'news.add_post'

    def get_success_url(self):
        return reverse_lazy('news_list')

    def form_valid(self, form):
        today_start = timezone.now().replace(hour=0, minute=0, second=0, microsecond=0)
        recent_posts = Post.objects.filter(
            author__user = self.request.user,
            created_at__gte=today_start,
        ).count()
        if recent_posts >= 3:
            messages.error(self.request, "Вы не можете публиковать более 3 новостей в сутки.")
            return self.form_invalid(form)

        post = form.save(commit=False)
        if self.request.path.startswith('/news/'):
            post.type = Post.NEWS
        elif self.request.path.startswith('/articles/'):
            post.type = Post.ARTICLE
        else:
            raise ValueError('Invalid post type')

        author, created = Author.objects.get_or_create(user=self.request.user)
        post.author = author
        post.save()
        form.save_m2m()
        self.send_notifications(post)
        return super().form_valid(form)

    def send_notifications(self, post):
        subscribers = set()
        for category in post.categories.all():
            for user in category.subscribers.all():
                if user.email:
                    subscribers.add(user)

        for user in subscribers:
            html_content = render_to_string(
                'news/email/new_post_notification.html',
                {
                    'post': post,
                    'user': user,
                }
            )
            msg = EmailMultiAlternatives(
                subject=post.title,
                body=f"{post.title}\n\n{post.content[:50]}...\n\nЗдравствуй, {user.username}. Новая статья в твоём любимом разделе!",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[user.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()


class PostUpdateView(PermissionRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'post_edit.html'
    permission_required = 'news.change_post'

    def get_success_url(self):
        return reverse_lazy('news_detail', kwargs={'pk': self.object.pk})


class PostDeleteView(DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news_list')


@login_required
def user_profile(request):
    user_display = request.user.get_full_name() or request.user.username or request.user.email
    is_author = request.user.groups.filter(name='authors').exists()
    return render(request, 'user_profile.html', {
        'user_display': user_display,
        'is_author': is_author
    })


@login_required
def upgrade_to_author(request):
    authors_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        authors_group.user_set.add(request.user)
        messages.success(request, 'Вы успешно стали автором')
    else:
        messages.info(request, 'Вы уже являетесь автором.')
    return redirect('user_profile')


@login_required
def subscribe(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    if request.user not in category.subscribers.all():
        category.subscribers.add(request.user)
    return redirect(request.META.get('HTTP_REFERER', 'news_list'))