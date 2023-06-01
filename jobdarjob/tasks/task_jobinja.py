from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from jobdarjob.celery import app


@app.task
def run_jobinja_link_spider():
    process = CrawlerProcess(get_project_settings())
    process.crawl('jobinja_link')
    process.start()


@app.task
def run_jobinja_single_spider():
    process = CrawlerProcess(get_project_settings())
    process.crawl('jobinja_single')
    process.start()
