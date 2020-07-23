from celery.schedules import crontab

from my_task.main import app

broker_url = "redis://127.0.0.1:6379/11"
result_backend = "redis://127.0.0.1:6379/12"

app.conf.beat_schedule = {
    'check_order_our_time': {
        'task': 'check_order',
        # 'schedule': 30.0,
        'schedule': crontab(),
        # 'args': (16, 16)
    },
}