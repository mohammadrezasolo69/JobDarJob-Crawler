from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from jobdarjob.celery import app


@app.task
def run_quera_link_spider():
    process = CrawlerProcess(get_project_settings())
    process.crawl('quera_link')
    process.start()


@app.task
def run_quera_single_spider():
    process = CrawlerProcess(get_project_settings())
    process.crawl('quera_single')
    process.start()
