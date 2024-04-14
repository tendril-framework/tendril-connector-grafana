
from ..aio import grafana
from grafana_client.client import GrafanaClientError

from tendril.utils import log
logger = log.get_logger(__name__)


async def check_create_folder(uid=None, parent_uid=None, title=None, team_id=None):
    try:
        existing = await grafana.folder.get_folder(uid)
        return existing['id']
    except GrafanaClientError as e:
        if e.status_code == 404:
            pass
        else:
            raise e

    response = await grafana.folder.create_folder(title=title, uid=uid, parent_uid=parent_uid)

    permissions = {'items': [
        {
            'role': "Editor",
            'permission': 2
        },
    ]}
    if team_id:
        permissions['items'].append(
            {
                'teamId': team_id,
                'permission': 1
            },
        )

    await grafana.folder.update_folder_permissions(uid=uid, items=permissions)
    return response['id']


async def get_folder_id(uid):
    existing = await grafana.folder.get_folder(uid)
    return existing['id']


async def find_folder_by_title(name, parent_uid=None):
    candidates = await grafana.folder.get_all_folders(parent_uid=parent_uid)
    for candidate in candidates:
        if candidate['title'] == name:
            return candidate['uid']
