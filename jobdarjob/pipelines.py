from jobdarjob.database.orm import ClickHouse

click = ClickHouse()


class JobinjaLinkPipeline:
    def process_item(self, item, spider):
        database = {
            "company_id": item.get('company_id'),
            "company_name": item.get('company_name'),
        }

        click.database.use('Jobdarjob')
        click.database.insert('jobinja_link', database)

        return item


class JobinjaSinglePipeline:
    def process_item(self, item, spider):
        database = {
            "link": item.get('link'),
            'label': item.get('label'),

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

        click.database.use('Jobdarjob')
        click.database.insert('jobinja_single', database)

        return item
