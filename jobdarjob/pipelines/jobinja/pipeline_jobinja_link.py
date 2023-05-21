from datetime import datetime

from jobdarjob.database import click


class JobinjaLinkPipeline:
    def process_item(self, item, spider):
        database = {
            "company_id": item.get('company_id'),
            "company_name": item.get('company_name'),
            "date_last_crawl": datetime.now().strftime('%Y/%m/%d'),
        }

        # click.database.use('Jobdarjob')
        click.database.insert('jobinja_link', database)
        click.database.optimize_table(table_name='jobinja_link', pk_field='company_id,company_name')

        return item
