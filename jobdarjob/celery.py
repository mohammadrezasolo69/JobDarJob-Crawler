from datetime import timedelta

from celery import Celery

app = Celery(main='jobdarjob', broker='redis://localhost:6379')
app.autodiscover_tasks(['jobdarjob.tasks'], force=True)

app.conf.beat_schedule = {
    'run_jobinja_link_spider': {
        'task': 'jobdarjob.tasks.run_jobinja_link_spider',
        'schedule': timedelta(days=1),
        'args': (),
    },
    'run_jobinja_single_spider': {
        'task': 'jobdarjob.tasks.run_jobinja_single_spider',
        'schedule': timedelta(days=1),
        'args': (),
        'relative': True,
    },
    'run_quera_link_spider': {
        'task': 'jobdarjob.tasks.run_quera_link_spider',
        'schedule': timedelta(days=1),
        'args': (),
    },
    'run_quera_single_spider': {
        'task': 'jobdarjob.tasks.run_quera_single_spider',
        'schedule': timedelta(days=1),
        'args': (),
        'relative': True,
    },
}
