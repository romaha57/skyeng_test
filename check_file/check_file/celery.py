import os

from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'check_file.settings')

app = Celery('check_file')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
