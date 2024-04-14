

from .variables import generate_variable
from .panel import generate_panel


class DashboardSpecBase(object):
    name = None
    title = None
    refresh = 'auto'
    timezone = 'browser'
    schema_version = 39

    def __init__(self, actual):
        self._actual = actual

    @property
    def container(self):
        return None

    @property
    def container_type(self):
        if self.container:
            return self.container.type_name

    @property
    def actual_type(self):
        return self._actual.type_name

    @property
    def variables_constant(self):
        return {}

    @property
    def variables_url(self):
        return {}

    @property
    def variables_query(self):
        return {}

    @property
    def panels(self):
        return []


async def generate_dashboard(spec):
    response = {}

    if spec.title:
        response['title'] = spec.title

    response.update({
        'tags': ['generated', spec.actual_type],
        'refresh': spec.refresh,
        'timezone': spec.timezone,
        'schemaVersion':  spec.schema_version,
    })

    constants = [await generate_variable(k, v, disallow_url=True) for k, v in spec.variables_constant.items()]
    variables = [await generate_variable(k, v) for k, v in spec.variables_url.items()]
    queries = [await generate_variable(k, v, disallow_url=True) for k, v in spec.variables_query.items()]

    if constants or variables or queries:
        response['templating'] = {}
        response['templating']['list'] = constants + variables + queries

    response['panels'] = [await generate_panel(x) for x in spec.panels]

    return response
