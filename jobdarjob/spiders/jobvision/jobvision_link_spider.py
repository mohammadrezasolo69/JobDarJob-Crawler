import re

import scrapy


class JobvisionLinkSpider(scrapy.Spider):
    name = 'jobvision_link'
    custom_settings = {
        'DOWNLOAD_TIMEOUT': 0
    }

    def start_requests(self):
        yield scrapy.Request('https://jobvision.ir/jobs', callback=self.parse, meta={"playwright": True})

    def parse(self, response, **kwargs):
        for item in response.xpath(
                '/html/body/app-root/div/app-jobs/section/div[2]/div[1]/div/div[1]/div/job-card-list/job-card'):

            link = item.xpath('a/@href').get()

            match = re.match(r"/jobs/(\d+)/", link)
            if match:
                company_id = match.group(1)

                yield {'company_id': company_id}
