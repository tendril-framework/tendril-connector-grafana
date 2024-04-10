

from grafana_client.client import GrafanaClientError
from ..aio import grafana_admin
from ..aio import grafana

from tendril.utils import log
logger = log.get_logger(__name__, log.DEBUG)


async def check_create_user(user_profile):
    try:
        user_email = user_profile['auth0']['email']
    except KeyError:
        raise AttributeError(f"Could not determine user email for user with id {user_profile['user_id']}")
    try:
        existing_user = await grafana_admin.users.find_user(user_email)
        # TODO Update existing user with profile if needed?
    except GrafanaClientError as e:
        if e.status_code == 404:
            pass
        else:
            raise e
    else:
        logger.debug(f"Found Grafana user with email {user_email}. Not creating.")
        return existing_user['id']

    logger.info(f"Creating Grafana user with email {user_email}")
    # TODO Detach Implementation from Auth0.
    user = {
        'name': user_profile['auth0']['name'],
        'email': user_email,
        'login': user_email,
        'password': user_profile['auth0']['user_id'],
    }
    result = await grafana_admin.admin.create_user(user)
    return result['id']

async def get_grafana_user_id(user):
    from tendril.authn.users import get_user_email
    user_email = get_user_email(user)
    try:
        existing_user = await grafana_admin.users.find_user(user_email)
        return existing_user['id']
    except GrafanaClientError as e:
        if e.status_code == 404:
            raise NameError(f"Did not find an existing grafana user with email {user_email}")

async def get_user_teams(grafana_user_id=None, user=None):
    if not grafana_user_id:
        if not user:
            raise AttributeError("Did not get a Grafana User ID or a Tendril User. One or the other is needed.")
        grafana_user_id = await get_grafana_user_id(user)
    else:
        if user:
            logger.warn("Got both a grafana user id and a tendril user id. Only one or the other should be provided. Using grafana user id.")
    # TODO Grafana client does not currently support get user teams?
    # https://grafana.com/docs/grafana/latest/developers/http_api/user/#get-teams-for-user
    # https://github.com/panodata/grafana-client/issues/171
    # teams = await grafana_admin.users.get_user(grafana_user_id)
    # logger.error(teams)
    return []