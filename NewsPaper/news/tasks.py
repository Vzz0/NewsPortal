from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta
from .models import Post, Category

@shared_task
def send_weekly_digest():
    end_date = timezone.now()
    start_date = end_date - timedelta(days=7)

    for category in Category.objects.all():
        posts = Post.objects.filter(
            categories=category,
            created_at__gte=start_date,
            created_at__lte=end_date
        ).distinct()

        if not posts.exists():
            continue

        for user in category.subscribers.all():
            if not user.email:
                continue

            html_content = render_to_string(
                'news/email/weekly_newsletter.html',
                {
                    'user': user,
                    'category': category,
                    'posts': posts,
                }
            )

            msg = EmailMultiAlternatives(
                subject=f'Новости за неделю: {category.name}',
                body=f'Привет, {user.username}! За последнюю неделю вышли новые статьи.',
                to=[user.email],
            )
            msg.attach_alternative(html_content, "text/html")
            msg.send()