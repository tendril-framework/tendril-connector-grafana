

from grafana_client.client import GrafanaBadInputError
from ..aio import grafana

from tendril.utils import log
logger = log.get_logger(__name__, log.DEBUG)


async def check_create_team(team_name, team_email=None):
    existing = await grafana.teams.get_team_by_name(team_name)
    if existing:
        if len(existing) > 1:
            raise ValueError(f"Got multiple results for team {team_name}. Expected only 1.")
        return existing[0]['id']
    logger.info(f"Creating Grafana team '{team_name}'.")
    created = await grafana.teams.add_team({'name': team_name, 'email': team_email})
    return created['teamId']


async def add_user_to_team(grafana_user_id, team_id):
    logger.debug(f"Adding grafana user {grafana_user_id} to team {team_id}.")
    try:
        result = await grafana.teams.add_team_member(team_id, grafana_user_id)
    except GrafanaBadInputError:
        return True
    return result
