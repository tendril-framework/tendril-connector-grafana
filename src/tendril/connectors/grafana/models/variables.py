

from inflection import humanize
from ..actions.datasources import get_datasource_backend


class QueriedVariable:
    datasource = 'db'
    query = None
    refresh = 1
    multi = False


async def generate_variable(key, value, disallow_url=False):
    response = {
        "label": humanize(key),
        "name": key,
        "hide": 2,
        "skipUrlSync": disallow_url,
    }
    if isinstance(value, QueriedVariable):
        if value.datasource == 'db':
            response['datasource'] = {
                'type': 'grafana-postgresql-datasource',
                'uid': await get_datasource_backend()
            }
        response.update({
            "description": "Spec Defined Query",
            "definition": value.query,
            "query": value.query,
            "refresh": value.refresh,
            "multi": False,
            "type": "query"
        })
    else:
        response.update({
            "description": "Spec Defined Constant",
            "query": value,
            "type": "constant"
        })
    return response
