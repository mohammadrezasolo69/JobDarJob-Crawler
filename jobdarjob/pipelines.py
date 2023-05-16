from jobdarjob.database.orm import ClickHouse
from scrapy.utils.project import get_project_settings

settings = get_project_settings()
Click = ClickHouse(host=settings.get('CLICKHOUSE_HOST'),port=settings.get('CLICKHOUSE_PORT'))



class JobinjaLinkPipeline:
    def process_item(self, item, spider):
        database = {
            "company_id": item.get('company_id'),
            "company_name": item.get('company_name'),
        }

        Click.database.use('Jobdarjob')
        Click.database.insert('jobinja_link', database)
        Click.database.optimize_table(table_name='jobinja_link', pk_field='company_id')


        return item


class JobinjaSinglePipeline:
    def process_item(self, item, spider):
        database = {
            "link": item.get('link'),
            'label': item.get('label'),
            "company_id": item.get('company_id'),

            "company_name": item.get('company_name'),
            "company_cover": item.get('company_cover'),
            "company_website": item.get('company_website'),
            "company_category": item.get('company_category'),

            "title": item.get('title'),
            "category": item.get('category'),
            "location": item.get('location'),
            "type_cooperation": item.get('type_cooperation'),
            "work_experience": item.get('work_experience'),
            "salary": item.get('salary'),
            "description": item.get('description'),
            "company_about": item.get('company_about'),
            "gender": item.get('gender'),
            "education": item.get('education'),
            "military_service": item.get('military_service'),
            "skills": item.get('skills'),
        }

        Click.database.use('Jobdarjob')
        Click.database.insert('jobinja_single', database)
        Click.database.optimize_table(table_name='jobinja_single', pk_field='company_id')

        return item
