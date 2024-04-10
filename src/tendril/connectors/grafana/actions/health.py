

from ..aio import grafana

from tendril.utils import log
logger = log.get_logger(__name__)


async def check():
    url = grafana.client.url
    logger.info(f"Using grafana at {url}")

    health = await grafana.health.check()
    logger.info("Grafana Health: ")
    logger.info(health)
