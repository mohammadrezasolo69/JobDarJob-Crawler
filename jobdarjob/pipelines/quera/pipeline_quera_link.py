from jobdarjob.database import click


class QueraLinkPipeline:
    def process_item(self, item, spider):
        insert_data = {
            "company_id": item.get('company_id'),
        }

        click.database.insert('quera_link', insert_data)
        click.database.optimize_table('quera_link',pk_field='company_id')

        return item
