

import inflection
from slugify import slugify
from tendril.connectors.grafana.actions.folders import check_create_folder
from .teams import ensure_graphs_team


def get_graphs_folder_path(interest_type, interest_name, descriptive_name=None):
    return [{'uid': slugify(interest_type), 'title': inflection.humanize(inflection.pluralize(interest_type))},
            {'uid': slugify(interest_name), 'title': descriptive_name}]


async def ensure_graphs_folder(*args, **kwargs):
    # TODO This is probably going to need a lot of non-trivial error handling.
    folder_path_parts = get_graphs_folder_path(*args, **kwargs)

    team_id = await ensure_graphs_team(interest_type=kwargs['interest_type'],
                                       interest_name=kwargs['interest_name'])

    folder_uid = None
    for idx, folder_spec in enumerate(folder_path_parts):
        if idx == len(folder_path_parts) - 1:
            await check_create_folder(parent_uid=folder_uid, team_id=team_id, **folder_spec)
        else:
            await check_create_folder(parent_uid=folder_uid, **folder_spec)
        folder_uid = folder_spec['uid']

    return folder_uid
