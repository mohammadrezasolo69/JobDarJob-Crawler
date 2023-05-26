import scrapy
from scrapy.loader import processors


class QueraLinkItem(scrapy.Item):
    company_id = scrapy.Field(
        input_processor=processors.Identity(),
        output_processor=processors.TakeFirst(),
    )
