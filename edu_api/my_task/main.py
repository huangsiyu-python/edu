import os

import django
from celery import Celery

app = Celery("edu")
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'edu_api.settings.develop')
django.setup()
app.config_from_object("my_task.config")

app.autodiscover_tasks(['my_task.sms','my_task.file','my_task.change_order'])

# 启动celery  在项目的跟目录下执行启动命令
# celery -A my_task.main worker --loglevel=info
