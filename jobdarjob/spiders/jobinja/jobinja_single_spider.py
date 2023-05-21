import re
import time
import scrapy
from scrapy.loader import ItemLoader
from jobdarjob.items import JobinjaSingleItem
from jobdarjob.database import click


class JobinjaSingleSpider(scrapy.Spider):
    name = 'jobinja_single'
    custom_settings = {
        'ITEM_PIPELINES': {
            'jobdarjob.pipelines.JobinjaSinglePipeline': 300,  # process item (insert data in db)
        },
    }

    def start_requests(self):
        data_from_jobinja_link = click.database.select(table_name='jobinja_link',columns=('company_name', 'company_id'))
        for data in data_from_jobinja_link:
            company_name, company_id = data
            link = f'https://jobinja.ir/companies/{company_name}/jobs/{company_id}/'
            yield scrapy.Request(link, callback=self.parse)

    def parse(self, response, **kwargs):
        loader = ItemLoader(item=JobinjaSingleItem(), response=response)
        # --------------------------------------------------------------------------------------------------------------
        link = response.url

        match = re.match(r"https://jobinja\.ir/companies/([\w-]+)/jobs/([\w-]+)", link)
        if match:
            loader.add_value('company_id', match.group(2))

        loader.add_value('label', 'jobinja')
        loader.add_value('link', link)

        # --------------------------------------------------------------------------------------------------------------

        loader.add_xpath('company_name', '//*[@id="view-job"]/div[1]/div[3]/div[1]/div/div/div/h2/text()')
        loader.add_xpath('company_cover', '//*[@id="view-job"]/div[1]/div[3]/div[1]/div/div/a/img/@src')
        loader.add_xpath('company_website', '//*[@id="view-job"]/div[1]/div[3]/div[1]/div/div/div/div/span[3]/a/@href')
        loader.add_xpath('company_category',
                         'normalize-space(//*[@id="view-job"]/div[1]/div[3]/div[1]/div/div/div/div/span[1]/a/text())')

        # --------------------------------------------------------------------------------------------------------------

        loader.add_xpath('title', '//*[@id="singleJob"]/div/div/div[1]/section/div[1]/div/h1/text()')
        loader.add_xpath('category', '//*[@id="singleJob"]/div/div/div[1]/section/ul[1]/li[1]/div/span/text()')
        loader.add_xpath('location',
                         'normalize-space(/html/body/div[1]/div[4]/div/div/div[1]/section/ul[1]/li[2]/div/span/text())')
        loader.add_xpath('type_cooperation',
                         'normalize-space(/html/body/div/div[4]/div/div/div[1]/section/ul[1]/li[3]/div/span/text())')
        loader.add_xpath('work_experience', '/html/body/div/div[4]/div/div/div[1]/section/ul[1]/li[4]/div/span/text()')
        loader.add_xpath('salary', '/html/body/div/div[4]/div/div/div[1]/section/ul[1]/li[5]/div/span/text()')
        loader.add_xpath('description', '/html/body/div/div[4]/div/div/div[1]/section/div[2]')
        loader.add_xpath('company_about', '/html/body/div/div[4]/div/div/div[1]/section/div[3]')

        # --------------------------------------------------------------------------------------------------------------

        loader.add_xpath('gender', '//*[@id="singleJob"]/div/div/div[1]/section/ul[2]/li[2]/div/span/text()')
        loader.add_xpath('education', '//*[@id="singleJob"]/div/div/div[1]/section/ul[2]/li[4]/div/span/text()')
        loader.add_xpath('military_service', '//*[@id="singleJob"]/div/div/div[1]/section/ul[2]/li[3]/div/span/@title')
        loader.add_xpath('skills', '//*[@id="singleJob"]/div/div/div[1]/section/ul[2]/li[1]/div/span/text()')

        # --------------------------------------------------------------------------------------------------------------

        yield loader.load_item()
