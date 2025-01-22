from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from fastapi_pundra.common.scheduler.schedule import bind_beat_schedule
from app.config.scheduler import schedules
from dotenv import load_dotenv

load_dotenv()

def create_celery_app(project_name: str, broker_type: str = 'redis'):
  app = Celery(project_name)
  app.conf.update(
    broker_url=os.getenv('CELERY_BROKER_URL'),
    result_backend=os.getenv('CELERY_RESULT_BACKEND'),
    timezone='UTC',
    enable_utc=True,
  )

  if broker_type == 'redis':
    app.conf.beat_scheduler = 'redbeat.RedBeatScheduler'
    app.conf.redbeat_redis_url = os.getenv('CELERY_BROKER_URL')

  app.autodiscover_tasks(['app.tasks', 'fastapi_pundra.common.mailer.task'])
  app.conf.beat_schedule = bind_beat_schedule(schedules=schedules) 

  return app