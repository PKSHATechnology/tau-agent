from tau.celery import app as celery_app
from tau.fastapi import app as fastapi_app

api = fastapi_app
worker = celery_app
