import scrapy
from scrapy.loader import processors

from jobdarjob.items.processors import clean_result, clean_description


class JobinjaSingleItem(scrapy.Item):
    link = scrapy.Field(
        input_processor=processors.MapCompose(clean_result), output_processor=processors.TakeFirst()
    )

    company_id = scrapy.Field(
        input_processor=processors.MapCompose(clean_result), output_processor=processors.TakeFirst()
    )

    label = scrapy.Field(
        input_processor=processors.MapCompose(clean_result), output_processor=processors.TakeFirst()
    )

    company_name = scrapy.Field(
        input_processor=processors.MapCompose(clean_result), output_processor=processors.TakeFirst()
    )

    company_cover = scrapy.Field(
        input_processor=processors.MapCompose(clean_result), output_processor=processors.TakeFirst()
    )
    company_website = scrapy.Field(
        input_processor=processors.MapCompose(clean_result), output_processor=processors.TakeFirst()
    )
    company_category = scrapy.Field(
        input_processor=processors.MapCompose(clean_result), output_processor=processors.TakeFirst()
    )

    # --------------------------------------------------------------------------------------------------------------

    title = scrapy.Field(
        input_processor=processors.MapCompose(clean_result), output_processor=processors.TakeFirst()
    )
    category = scrapy.Field(
        input_processor=processors.MapCompose(clean_result), output_processor=processors.TakeFirst()
    )
    location = scrapy.Field(
        input_processor=processors.MapCompose(clean_result), output_processor=processors.TakeFirst()
    )
    type_cooperation = scrapy.Field(
        input_processor=processors.MapCompose(clean_result), output_processor=processors.TakeFirst()
    )
    work_experience = scrapy.Field(
        input_processor=processors.MapCompose(clean_result), output_processor=processors.TakeFirst()
    )
    salary = scrapy.Field(
        input_processor=processors.MapCompose(clean_result), output_processor=processors.TakeFirst()
    )
    description = scrapy.Field(
        input_processor=processors.MapCompose(clean_description),
        output_processor=processors.TakeFirst()
    )
    company_about = scrapy.Field(
        input_processor=processors.MapCompose(clean_description), output_processor=processors.TakeFirst()
    )

    # --------------------------------------------------------------------------------------------------------------

    gender = scrapy.Field(
        input_processor=processors.MapCompose(clean_result), output_processor=processors.TakeFirst()
    )
    education = scrapy.Field(
        input_processor=processors.MapCompose(clean_result), output_processor=processors.TakeFirst()
    )
    military_service = scrapy.Field(
        input_processor=processors.MapCompose(clean_result), output_processor=processors.TakeFirst()
    )
    skills = scrapy.Field(
        input_processor=processors.MapCompose(clean_result),
        output_processor=processors.Identity()
    )

    publication_date = scrapy.Field(
        input_processor=processors.Identity(),
        output_processor=processors.Identity()
    )
