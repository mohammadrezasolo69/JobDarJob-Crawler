from datetime import datetime

from jobdarjob.database import click


class JobdarjobSinglePipeline:
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
            "publication_date": item.get('publication_date'),
            "date_last_crawl": datetime.now().strftime('%Y/%m/%d'),

        }

        click.database.insert('jobdarjob_single', database)
        click.database.optimize_table(table_name='jobdarjob_single', pk_field='id')

        return item
