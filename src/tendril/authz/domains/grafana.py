

from tendril.authz.domains.base import AuthzDomainBase
from tendril.core.topology.grafana.teams import get_team_name
from tendril.core.topology.grafana.teams import get_team_email
from tendril.connectors.grafana.actions.users import check_create_user
from tendril.connectors.grafana.actions.users import get_user_teams
from tendril.connectors.grafana.actions.teams import add_user_to_team
from tendril.core.topology.grafana.teams import ensure_graphs_team
from tendril.common.interests.memberships import user_memberships
from tendril.config import GRAFANA_TEAM_COMPOSITION

from tendril.utils import log
logger = log.get_logger(__name__)


class GrafanaAuthzDomain(AuthzDomainBase):
    def _get_target_teams(self, user):
        # TODO This needs to also return memberships where the user has access to a child
        #   but not necessarily at the team level. Don't use memberships directly, though.
        #   It will be wasteful. Traverse the allowed_children tree and find specific
        #   non-inherited interests which will trigger inclusion in the team associated with
        #   the defined interest type.
        search_itypes = [x[0] for x in GRAFANA_TEAM_COMPOSITION]
        memberships = user_memberships(
            user, interest_types=search_itypes,
            include_inherited=True, include_delegated=False,
            include_statuses=['ACTIVE'],
        )
        target_teams =  memberships.df.select(['type', 'interest.name']).unique()
        return [{'interest_type': row[0], 'interest_name': row[1]} for row in target_teams.rows()]

    async def upsert(self, user, first_login):
        user_profile = self.get_user_profile(user.puid)
        grafana_user_id = await check_create_user(user_profile)

        # Get target teams
        target_teams = self._get_target_teams(user)

        # Create teams if necessary
        for team_info in target_teams:
            team_info['team_id'] = await ensure_graphs_team(**team_info)

        current_user_team_ids = await get_user_teams(grafana_user_id=grafana_user_id)

        for team_info in target_teams:
            if team_info['team_id'] not in current_user_team_ids:
                await add_user_to_team(grafana_user_id, team_info['team_id'])

        # TODO Remove teams not in list?


domains = {
    'grafana': GrafanaAuthzDomain()
}
