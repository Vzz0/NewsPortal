from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'get_categories', 'type', 'created_at', 'rating')
    list_filter = ('type', 'created_at', 'author')
    search_fields = ('title', 'content')
    date_hierarchy = 'created_at'

    def get_categories(self, obj):
        return ", ".join([cat.name for cat in obj.categories.all()]) or "—"

    get_categories.short_description = 'Категории'  # Заголовок колонки
    get_categories.admin_order_field = 'categories'  # Сортировка (частично работает)


class AuthorAdmin(admin.ModelAdmin):
    list_display = ('user', 'rating')
    search_fields = ('user__username',)


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'get_subscribers_count')
    search_fields = ('name',)

    def get_subscribers_count(self, obj):
        return obj.subscribers.count()

    get_subscribers_count.short_description = 'Подписчиков'


class PostCategoryAdmin(admin.ModelAdmin):
    list_display = ('post', 'category')
    list_filter = ('category',)
    search_fields = ('post__title', 'category__name')


class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'created_at', 'rating')
    list_filter = ('created_at', 'rating')
    search_fields = ('text', 'user__username')


# Регистрация моделей
admin.site.register(Author, AuthorAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(PostCategory, PostCategoryAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Post, PostAdmin)