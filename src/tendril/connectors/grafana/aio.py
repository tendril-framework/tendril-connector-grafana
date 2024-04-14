

from grafana_client import AsyncGrafanaApi
from grafana_client import TokenAuth

from tendril.config import GRAFANA_SERVER_HOST
from tendril.config import GRAFANA_SERVER_PORT
from tendril.config import GRAFANA_SERVER_SSL
from tendril.config import GRAFANA_PROVISIONER_TOKEN
from tendril.config import GRAFANA_ORG
from tendril.config import GRAFANA_ADMIN_USER
from tendril.config import GRAFANA_ADMIN_PASSWORD

from tendril.utils.log import get_logger
logger = get_logger(__name__)


if GRAFANA_SERVER_SSL:
    scheme = 'https'
else:
    scheme = 'http'


grafana = AsyncGrafanaApi(
    host=GRAFANA_SERVER_HOST,
    port=GRAFANA_SERVER_PORT,
    protocol=scheme,
    auth=TokenAuth(token=GRAFANA_PROVISIONER_TOKEN),
    organization_id=GRAFANA_ORG)


grafana_admin = AsyncGrafanaApi(
    host=GRAFANA_SERVER_HOST,
    port=GRAFANA_SERVER_PORT,
    protocol=scheme,
    auth=(GRAFANA_ADMIN_USER, GRAFANA_ADMIN_PASSWORD)
)

logger.info(f"Using grafana at {grafana.client.url}")
