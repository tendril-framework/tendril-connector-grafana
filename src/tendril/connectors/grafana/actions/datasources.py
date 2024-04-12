

from ..aio import grafana

from tendril.config import GRAFANA_DATASOURCE_INFLUXDB_MONITORS
from tendril.config import GRAFANA_DATASOURCE_BACKEND_READER


async def get_datasources():
    result = await grafana.datasource.list_datasources()
    return result


async def get_datasource(name):
    datasources = await get_datasources()
    for datasource in datasources:
        if datasource['name'] == name:
            return datasource


async def get_datasource_uid(name):
    datasource = await get_datasource(name)
    return datasource['uid']


async def get_datasource_monitors():
    if not GRAFANA_DATASOURCE_INFLUXDB_MONITORS:
        raise ValueError("Monitors InfluxDB datasource not configured for Grafana")
    datasource = await get_datasource(GRAFANA_DATASOURCE_INFLUXDB_MONITORS)
    return datasource['uid']


async def get_datasource_backend():
    if not GRAFANA_DATASOURCE_BACKEND_READER:
        raise ValueError("Backend Reader datasource not configured for Grafana")
    datasource = await get_datasource(GRAFANA_DATASOURCE_BACKEND_READER)
    return datasource['uid']
