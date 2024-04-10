

from ..aio import grafana_admin


def get_datasources():
    return grafana_admin.datasource.list_datasources()
