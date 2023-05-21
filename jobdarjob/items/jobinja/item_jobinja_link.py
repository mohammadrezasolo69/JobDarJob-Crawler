import scrapy
from scrapy.loader import processors

from jobdarjob.items.processors import clean_result


class JobdarjobLinkItem(scrapy.Item):
    company_name = scrapy.Field(
        input_processor=processors.MapCompose(clean_result), output_processor=processors.TakeFirst()
    )
    company_id = scrapy.Field(
        input_processor=processors.MapCompose(clean_result), output_processor=processors.TakeFirst()
    )