

import inflection
from tendril.connectors.grafana.actions.teams import check_create_team
from tendril.config import GRAFANA_TEAM_EMAIL_DOMAIN


def get_team_name(interest_type, interest_name):
    return f"{inflection.humanize(interest_type)} {interest_name}"


def get_team_email(interest_type, interest_name):
    return f"{inflection.dasherize(interest_name)}@{inflection.underscore(inflection.pluralize(interest_type))}{GRAFANA_TEAM_EMAIL_DOMAIN}"


async def ensure_graphs_team(*args, **kwargs):
    team_name = get_team_name(*args, **kwargs)
    team_email = get_team_email(*args, **kwargs)
    team_id = await check_create_team(team_name, team_email)
    return team_id
