import re

from scrapy import spiders
from scrapy.loader import ItemLoader

from jobdarjob.items.quera import QueraLinkItem


class QueraLinkSpider(spiders.Spider):
    name = 'quera_link'
    page = 1
    last_page = None

    start_urls = [
        'https://quera.org/magnet/jobs',
    ]

    def parse(self, response, **kwargs):
        # Extract the last page number
        self.last_page = response.xpath('//button[@class="chakra-button css-g3korc"]/text()')[-1].get()

        # Processing the desired items
        for item in response.xpath('/html/body/div[5]/div[2]/main/section/div[2]/article'):
            loader = ItemLoader(item=QueraLinkItem(), response=item)
            url = item.xpath('div/div/div[2]/div[1]/h2/a/@href').get()

            regex = r'\/jobs\/([^\/]+)$'
            match = re.search(regex, url)
            if match:
                company_id = match.group(1)
                loader.add_value('company_id', company_id)

            yield loader.load_item()

        # pagination
        next_page = f'{self.start_urls[0]}?page={str(self.page)}'
        if self.page != int(self.last_page):
            yield response.follow(next_page, callback=self.parse)
            self.page += 1
