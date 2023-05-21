from jobdarjob.database import click


# ------------------------------------------ Jobinja -------------------------------------------------
# Link
schema_table = {
    'company_id': 'String',
    'company_name': 'String',
    'date_last_crawl': 'Date'
}
click.database.create_tabel(table_name='jobinja_link', fields=schema_table, engine='ReplacingMergeTree',
                            primary_key=('company_id',))