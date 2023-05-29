import scrapy


class JobvisionLinkSpider(scrapy.Spider):
    name = 'jobvision_link'
    start_urls = [
        'https://jobvision.ir/jobs',
        ]

    def parse(self, response, **kwargs):
        ...