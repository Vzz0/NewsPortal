# Импортируем необходимые модели
from news.models import Author, Category, Post, PostCategory, Comment
from django.contrib.auth.models import User

# Создаем двух пользователей
user1 = User.objects.create_user(username='user1', password='password1')
user2 = User.objects.create_user(username='user2', password='password2')

# Создаем двух авторов, связанных с пользователями
author1 = Author.objects.create(user=user1)
author2 = Author.objects.create(user=user2)

# Добавляем 4 категории
category1 = Category.objects.create(name='Спорт')
category2 = Category.objects.create(name='Политика')
category3 = Category.objects.create(name='Образование')
category4 = Category.objects.create(name='Наука')

# Добавляем 2 статьи и 1 новость
post1 = Post.objects.create(
    author=author1,
    type=Post.ARTICLE,
    title='Статья про спорт',
    content='Это первая статья про спорт...',
    rating=0
)
post2 = Post.objects.create(
    author=author2,
    type=Post.ARTICLE,
    title='Статья про политику',
    content='Это вторая статья про политику...',
    rating=0
)
news1 = Post.objects.create(
    author=author1,
    type=Post.NEWS,
    title='Новость про образование',
    content='Это новость про образование...',
    rating=0
)

# Присваиваем категории статьям/новостям
PostCategory.objects.create(post=post1, category=category1)
PostCategory.objects.create(post=post1, category=category2)  # Статья про спорт имеет две категории
PostCategory.objects.create(post=post2, category=category2)
PostCategory.objects.create(post=news1, category=category3)

# Создаем комментарии
comment1 = Comment.objects.create(post=post1, user=user1, text='Хорошая статья!', rating=0)
comment2 = Comment.objects.create(post=post1, user=user2, text='Не согласен...', rating=0)
comment3 = Comment.objects.create(post=post2, user=user1, text='Интересно!', rating=0)
comment4 = Comment.objects.create(post=news1, user=user2, text='Спасибо за новость!', rating=0)

# Применяем функции like() и dislike() к статьям/новостям и комментариям
post1.like()
post1.like()
post2.dislike()
news1.like()

comment1.like()
comment2.dislike()
comment3.like()
comment4.like()

# Обновляем рейтинги пользователей
author1.update_rating()
author2.update_rating()

# Выводим username и рейтинг лучшего пользователя
best_author = Author.objects.order_by('-rating').first()
print(f"Лучший пользователь: {best_author.user.username}, Рейтинг: {best_author.rating}")

# Выводим дату добавления, username автора, рейтинг, заголовок и превью лучшей статьи
best_post = Post.objects.filter(type=Post.ARTICLE).order_by('-rating').first()
print(f"Дата: {best_post.created_at}")
print(f"Автор: {best_post.author.user.username}")
print(f"Рейтинг: {best_post.rating}")
print(f"Заголовок: {best_post.title}")
print(f"Превью: {best_post.preview()}")

# Выводим все комментарии к этой статье
comments_for_best_post = Comment.objects.filter(post=best_post)
for comment in comments_for_best_post:
    print(f"Дата: {comment.created_at}, Пользователь: {comment.user.username}, Рейтинг: {comment.rating}, Текст: {comment.text}")