import os
from celery import Celery

# set the default Django settings module for the 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')  # Creating an instance of the application

# Loading any custom configuration from project settings
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

