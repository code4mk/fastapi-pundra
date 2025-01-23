from __future__ import absolute_import, unicode_literals
import os
from typing import List
from celery import Celery
from fastapi_pundra.common.scheduler.schedule import bind_beat_schedule
from app.config.scheduler import schedules
from dotenv import load_dotenv

load_dotenv()

def create_celery_app(project_name: str, task_modules: List[str] | str = [], broker_type: str = 'redis'):
  # Convert task_modules to list if it's a string
  if isinstance(task_modules, str):
    task_modules = [task_modules]

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

  # Combine default task modules with provided task modules
  default_task_modules = ['fastapi_pundra.common.mailer.task']
  all_task_modules = default_task_modules + task_modules
  app.autodiscover_tasks(all_task_modules)

  app.conf.beat_schedule = bind_beat_schedule(schedules=schedules) 

  return app