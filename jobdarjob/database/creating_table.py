from scrapy.utils.project import get_project_settings
from orm import ClickHouseModel

# Connect to clickhouse
settings = get_project_settings()
Click = ClickHouseModel(host=settings.get('CLICKHOUSE_HOST'), port=settings.get('CLICKHOUSE_PORT'))

# create table Jobdarjob
Click.database.create_db(database_name='Jobdarjob', using=True)

# ------------------------------------------ Jobinja -------------------------------------------------
# Link
schema_table = {
    'company_id': 'String',
    'company_name': 'String',
    'date_last_crawl': 'Date'
}
Click.database.create_tabel(table_name='jobinja_link', fields=schema_table, engine='ReplacingMergeTree',
                            primary_key=('company_id',))

# Single
schema_table = {
    'id': 'UUID DEFAULT generateUUIDv4()',
    'company_id': 'String',
    "link": 'String',
    'label': 'String',
    "company_name": 'String',
    "company_cover": 'String',
    "company_website": 'Nullable(String)',
    "company_category": 'String',
    "title": 'String',
    "category": 'String',
    "location": 'String',
    "type_cooperation": 'String',
    "work_experience": 'String',
    "salary": 'String',
    "description": 'String',
    "company_about": 'String',
    "gender": 'String',
    "education": 'String',
    "military_service": 'String',
    "skills": 'Array(Nullable(String))',
    'date_last_crawl': 'Date'
}
Click.database.create_tabel(table_name='jobinja_single', fields=schema_table, engine='ReplacingMergeTree',
                            primary_key=('id',)
                            )
