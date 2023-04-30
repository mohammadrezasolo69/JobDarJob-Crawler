import scrapy
from itemloaders import processors


class JobdarjobListItem(scrapy.Item):
    company_name = scrapy.Field(input_processor=processors.Identity(), output_processor=processors.TakeFirst())
    company_id = scrapy.Field(input_processor=processors.Identity(), output_processor=processors.TakeFirst())
