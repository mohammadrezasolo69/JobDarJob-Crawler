import re
import time
import scrapy
from scrapy.loader import ItemLoader
from jobdarjob.items.jobinja import JobdarjobLinkItem


class JobinjaLinkSpider(scrapy.Spider):
    name = "jobinja_link"
    start_urls = [
        "https://jobinja.ir/jobs"
    ]

    custom_settings = {
        'ITEM_PIPELINES': {
            'jobdarjob.pipelines.jobinja.JobinjaLinkPipeline': 300,  # process item (insert data in db)
        },
    }

    def parse(self, response, **kwargs):
        for item in response.xpath('/html/body/div[1]/div[3]/form[2]/div/div/div[2]/section/div/ul/li'):
            loader = ItemLoader(item=JobdarjobLinkItem(), selector=item)

            link = item.xpath('div/div[1]/a/@href').get()

            match = re.match(r"https://jobinja\.ir/companies/([\w-]+)/jobs/([\w-]+)", link)
            if match:
                loader.add_value('company_name', match.group(1))
                loader.add_value('company_id', match.group(2))

            yield loader.load_item()

        # pagination
        next_page = response.css('div.paginator a[rel="next"]::attr(href)').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)