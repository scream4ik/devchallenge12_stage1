import celery
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'devchallenge.settings')

app = celery.Celery('devchallenge')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
