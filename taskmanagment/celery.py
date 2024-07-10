import os
from django.conf import settings
from celery import Celery
# from celery import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "taskmanagment.settings")

app = Celery("taskmanagment")

app.config_from_object("django.conf:settings", namespace="CELERY")

app.autodiscover_tasks()


@app.task(bind=True, ignore_result=True)
def debug_task(self):
    print(f'Request: {self.request!r}')



# app.conf.beat_schedule = {
#     'daily-task': {
#         'task': 'your_app_name.tasks.daily_task',
#         'schedule': crontab(hour="0", minute="0"),  # Ежедневно в полночь
#     },
# }
