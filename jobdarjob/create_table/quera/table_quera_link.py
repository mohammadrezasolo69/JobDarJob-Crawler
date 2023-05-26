from jobdarjob.database import click

# ------------------------------------------ Quera -------------------------------------------------
# Link
schema_table = {
    'company_id': 'String',
}
click.database.create_tabel(table_name='quera_link', fields=schema_table, engine='ReplacingMergeTree',
                            primary_key=('company_id',))
