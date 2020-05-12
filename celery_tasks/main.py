# 1.导包Celery
from celery import Celery

# 2.配置celery可能加载到的美多项目的包
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pets_forum.settings")

# 3.创建celery实例
celery_app = Celery('celery_tasks')

# 4.加载celery配置
celery_app.config_from_object('celery_tasks.config')
celery_app.autodiscover_tasks(['celery_tasks.email'])