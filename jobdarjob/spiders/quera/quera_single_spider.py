import scrapy
from scrapy import Request
from scrapy.loader import ItemLoader

from jobdarjob.database import click
from jobdarjob.items.quera import QueraSingleItem


class QueraSingleSpider(scrapy.Spider):
    name = 'quera_single'

    # start_urls = [
    #     'https://quera.org/magnet/jobs/x7pv9',
    #     # 'https://quera.org/magnet/jobs/jq978',
    # ]

    # custom_settings = {
    #     'ITEM_PIPELINES': {
    #         'jobdarjob.pipelines.JobdarjobSinglePipeline': 300,  # process item (insert data in db)
    #     },
    # }

    def start_requests(self):
        company_ids = click.database.select('quera_link', ('company_id',))
        for company_id in company_ids:
            url = f'https://quera.org/magnet/jobs/{company_id[0]}'
            yield Request(url, callback=self.parse)

    def parse(self, response, **kwargs):
        loader = ItemLoader(item=QueraSingleItem(), response=response)
        # --------------------------------------------------------------------------------------------------------------
        loader.add_value('label', 'quera')
        loader.add_value('link', response.url)

        # --------------------------------------------------------------------------------------------------------------
        loader.add_xpath('publication_date',
                         '//*[@id="__next"]/div[2]/main/div/aside/div/div[1]/div[2]/div[1]/div[contains(@class, "chakra-stack") and @title]/div[1]/p/text()')

        loader.add_xpath('company_name', '//*[@id="__next"]/div[2]/header/div/div[1]/div[2]/div/div[1]/div[1]/a/text()')
        loader.add_xpath('company_cover', '//*[@id="__next"]/div[2]/header/div/div[1]/div[2]/img/@src')
        loader.add_xpath('company_website', '//*[@id="view-job"]/div[1]/div[3]/div[1]/div/div/div/div/span[3]/a/@href')
        loader.add_value('company_category', '')

        # --------------------------------------------------------------------------------------------------------------

        loader.add_xpath('title', '//*[@id="__next"]/div[2]/header/div/div[1]/div[2]/div/div[1]/h1/text()')
        loader.add_xpath('category',
                         '//*[@id="__next"]/div[2]/main/div/aside/div/div[1]/div[1]/div/div[2]/div[1]/p/text()')
        loader.add_xpath('location',
                         '//*[@id="__next"]/div[2]/header/div/div[1]/div[2]/div/div[1]/div[2]/div/div/span/text()')
        loader.add_xpath('type_cooperation',
                         '//*[@id="__next"]/div[2]/main/div/aside/div/div[1]/div[2]/div[1]/div[1]/div/p/text()')
        loader.add_xpath('work_experience',
                         '//*[@id="__next"]/div[2]/main/div/aside/div/div[1]/div[2]/div[1]/div[2]/div/p/text()')
        loader.add_xpath('salary',
                         '//*[@id="__next"]/div[2]/main/div/aside/div/div[1]/div[2]/div[1]/div[4]/div/p/text()')
        loader.add_xpath('description', '//*[@id="__next"]/div[2]/main/section/div/div[3]/div/div')
        loader.add_xpath('company_about', '//*[@id="__next"]/div[2]/main/section/div/div[2]/div/div')

        # --------------------------------------------------------------------------------------------------------------

        loader.add_value('gender', '')
        loader.add_value('education', '')
        loader.add_value('military_service', '')

        loader.add_xpath('skills', '//*[@id="__next"]/div[2]/main/section/div/div[1]/div/div/ul/span/span')

        yield loader.load_item()
