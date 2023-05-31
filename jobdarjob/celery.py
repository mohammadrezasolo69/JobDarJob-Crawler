from celery import Celery

app = Celery(main='jobdarjob', broker='redis://localhost:6379')

