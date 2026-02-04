import os
import django
import random
from datetime import timedelta
from django.utils import timezone

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPaper.settings')
django.setup()

from django.contrib.auth.models import User
from news.models import Author, Category, Post, Comment

# ============ ДАННЫЕ ДЛЯ ГЕНЕРАЦИИ ============
USERNAMES = ['ivan', 'maria', 'alex', 'olga', 'dmitry', 'anna', 'sergey', 'elena']
CATEGORIES = ['Политика', 'Экономика', 'Спорт', 'Культура', 'Наука', 'Технологии', 'Образование', 'Здоровье']
TITLES_NEWS = [
    'Срочно: {}', 'Важно: {}', 'Сегодня: {}', 'Сообщают: {}', 'Анонс: {}',
    'Эксклюзив: {}', 'Официально: {}', 'Аналитика: {}'
]
TITLES_ARTICLES = [
    'Как {}: практическое руководство', 'Почему {} важнее, чем кажется',
    '10 фактов о {}', 'История {}: от истоков до наших дней',
    'Будущее {}: прогнозы экспертов', 'Мифы и реальность о {}',
    'Как {} влияет на нашу жизнь', 'Неочевидные аспекты {}'
]
CONTENT_TOPICS = [
    'искусственный интеллект', 'криптовалюты', 'климатические изменения', 'космические исследования',
    'олимпийские игры', 'выборы президента', 'цифровая экономика', 'генетические исследования',
    'кибербезопасность', 'возобновляемая энергия', 'робототехника', 'пандемия гриппа',
    'международные санкции', 'инфляция в стране', 'новые законы', 'стартапы в России',
    'футбольный чемпионат', 'театральная премьера', 'археологические находки', 'квантовые компьютеры'
]

# ============ 1. ОЧИСТКА СТАРЫХ ДАННЫХ ============
print("🧹 Очистка базы данных...")
Comment.objects.all().delete()
Post.objects.all().delete()
PostCategory = Post.categories.through
PostCategory.objects.all().delete()
Author.objects.all().delete()
User.objects.filter(is_superuser=False).delete()
Category.objects.all().delete()

# ============ 2. СОЗДАНИЕ КАТЕГОРИЙ ============
print("📚 Создание категорий...")
categories = {}
for name in CATEGORIES:
    cat, _ = Category.objects.get_or_create(name=name)
    categories[name] = cat
    print(f"  → {name}")

# ============ 3. СОЗДАНИЕ ПОЛЬЗОВАТЕЛЕЙ И АВТОРОВ ============
print("\n👤 Создание пользователей и авторов...")
authors = []
for username in USERNAMES:
    user = User.objects.create_user(
        username=username,
        email=f"{username}@example.com",
        password="password123"
    )
    author = Author.objects.create(user=user, rating=random.randint(50, 200))
    authors.append(author)
    print(f"  → {username} (рейтинг: {author.rating})")

# ============ 4. СОЗДАНИЕ ПОСТОВ ============
print("\n🗞️ Создание постов...")

def generate_content(topic, length=500):
    paragraphs = [
        f"В последнее время тема {topic} привлекает всё больше внимания экспертов и обычных граждан.",
        f"Исследования показывают, что {topic} оказывает значительное влияние на различные сферы жизни.",
        f"Многие компании активно инвестируют в развитие {topic}, прогнозируя рост рынка на 30% в ближайшие годы.",
        f"Однако существуют и риски, связанные с {topic}, которые требуют внимательного анализа.",
        f"Эксперты рекомендуют следить за новостями в области {topic} и адаптироваться к изменениям."
    ]
    content = " ".join(random.sample(paragraphs, min(3, len(paragraphs))))
    return content + " " + content[:length - len(content)]

# 100 новостей
for i in range(1, 101):
    topic = random.choice(CONTENT_TOPICS)
    title = random.choice(TITLES_NEWS).format(f"события в сфере {topic}")
    post = Post.objects.create(
        author=random.choice(authors),
        type=Post.NEWS,
        title=title,
        content=generate_content(topic, 300),
        rating=random.randint(0, 50),
        created_at=timezone.now() - timedelta(days=random.randint(0, 30))
    )
    post.categories.add(random.choice(list(categories.values())))
    print(f"  [Новость #{i}] {title[:50]}...")

# 100 статей
for i in range(1, 101):
    topic = random.choice(CONTENT_TOPICS)
    title = random.choice(TITLES_ARTICLES).format(topic)
    post = Post.objects.create(
        author=random.choice(authors),
        type=Post.ARTICLE,
        title=title,
        content=generate_content(topic, 800),
        rating=random.randint(20, 100),
        created_at=timezone.now() - timedelta(days=random.randint(0, 60))
    )
    # Добавляем 1-3 категории
    cats = random.sample(list(categories.values()), k=random.randint(1, 3))
    post.categories.add(*cats)
    print(f"  [Статья #{i}] {title[:50]}...")

# ============ 5. СОЗДАНИЕ КОММЕНТАРИЕВ ============
print("\n💬 Создание комментариев...")
posts = list(Post.objects.all())
users = list(User.objects.all())

for i in range(300):  # 300 комментариев
    post = random.choice(posts)
    user = random.choice(users)
    comment = Comment.objects.create(
        post=post,
        user=user,
        text=f"Интересная публикация о {random.choice(CONTENT_TOPICS)}. Спасибо за материал!",
        rating=random.randint(-5, 20)
    )
    if i % 50 == 0:
        print(f"  → Создано {i} комментариев...")

# ============ 6. ПОДПИСКИ НА КАТЕГОРИИ ============
print("\n🔔 Назначение подписок на категории...")
for user in users[:5]:  # Первые 5 пользователей подписываются
    cats = random.sample(list(categories.values()), k=random.randint(2, 4))
    for cat in cats:
        cat.subscribers.add(user)
    print(f"  → {user.username} подписан на: {', '.join([c.name for c in cats])}")

# ============ 7. ОБНОВЛЕНИЕ РЕЙТИНГОВ АВТОРОВ ============
print("\n📈 Обновление рейтингов авторов...")
for author in authors:
    author.update_rating()
    print(f"  → {author.user.username}: рейтинг = {author.rating}")

print("\n✅ База данных успешно наполнена!")
print(f"   • Категории: {Category.objects.count()}")
print(f"   • Авторы: {Author.objects.count()}")
print(f"   • Новости: {Post.objects.filter(type=Post.NEWS).count()}")
print(f"   • Статьи: {Post.objects.filter(type=Post.ARTICLE).count()}")
print(f"   • Комментарии: {Comment.objects.count()}")