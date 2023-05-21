from scrapy.utils.project import get_project_settings
from jobdarjob.database.interface import ClickHouseModel

setting = get_project_settings()

click = ClickHouseModel(host=setting.get('CLICKHOUSE_HOST'), port=setting.get('CLICKHOUSE_PORT'))

try:
    click.database.use(database_name=setting.get('CLICKHOUSE_DATABASE'))
except:
    click.database.create_db(database_name=setting.get('CLICKHOUSE_DATABASE'))
