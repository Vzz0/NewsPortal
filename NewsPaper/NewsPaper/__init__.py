
from .celery import app as celery_app

default_app_config = 'NewsPaper.apps.NewsPaperConfig'
celery = celery_app

__all__ = ('celery_app', 'celery')