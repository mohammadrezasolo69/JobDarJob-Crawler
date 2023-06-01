from celery import Celery

app = Celery(main='jobdarjob', broker='redis://localhost:6379')
app.autodiscover_tasks(['jobdarjob.tasks'], force=True)
