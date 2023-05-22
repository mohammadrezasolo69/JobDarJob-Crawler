from jobdarjob.database import click

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
    'date_last_crawl': 'Date',
    "publication_date": "Int8"
}
click.database.create_tabel(table_name='jobinja_single', fields=schema_table, engine='ReplacingMergeTree',
                            primary_key=('id',)
                            )
