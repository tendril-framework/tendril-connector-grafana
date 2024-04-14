

from grafana_client.client import GrafanaClientError
from ..aio import grafana


async def search_dashboards(folder_uids=None, tags=None, type_="dash-db"):
    response = await grafana.search.search_dashboards(type_=type_, tag=tags,
                                                      folder_uids=folder_uids)


async def get_dashboard(uid):
    try:
        response = await grafana.dashboard.get_dashboard(uid)
        return response
    except GrafanaClientError as e:
        if e.status_code == 404:
            return None
        raise e


async def upsert_dashboard(dashboard_model, team_id=None, folder_uid=None, commit_msg=None, overwrite=True):
    if 'uid' in dashboard_model and dashboard_model['uid']:
        existing = await get_dashboard(dashboard_model['uid'])
        if existing:
            dashboard_model['id'] = existing['id']
            if not folder_uid:
                folder_uid = existing['meta']['folderUid']

    dashboard_model.setdefault('id', None)
    dashboard_model.setdefault('uid', None)
    dashboard_model.setdefault('tags', ['generated'])
    dashboard_model.setdefault('timezone', 'browser')
    dashboard_model.setdefault('refresh', '60s')

    payload = {
        'dashboard': dashboard_model,
        'folderUid': folder_uid,
        'message': commit_msg or "",
        'oerwrite': overwrite
    }

    response = await grafana.dashboard.update_dashboard(payload)

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

    await grafana.dashboard.update_permissions_generic(response['uid'],
                                                       items=permissions)
    return response
