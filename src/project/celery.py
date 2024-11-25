import os

from celery import Celery

# Determine the settings file based on the environment variable
settings_module = os.getenv('DJANGO_SETTINGS_MODULE', 'project.settings.local')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', settings_module)

app = Celery('project')

# Ensure envs start with 'CELERY_' namespace for Celery-related settings
app.config_from_object('django.conf:settings', namespace='CELERY')
# automatically discover tasks
app.autodiscover_tasks()
