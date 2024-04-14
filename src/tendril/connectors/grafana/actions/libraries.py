

from ..aio import grafana
from .folders import find_folder_by_title
from .folders import get_folder_id
from tendril.config import GRAFANA_LIBRARIES_FOLDER


async def find_library_root_folder():
    result = await find_folder_by_title(GRAFANA_LIBRARIES_FOLDER)
    return result


async def find_library_folder(name):
    library_root = await find_library_root_folder()
    result = await find_folder_by_title(name, parent_uid=library_root)
    return result


async def list_library_panels(libraries=None):
    if libraries:
        libraries = ",".join([str(x) for x in [await get_folder_id(await find_library_folder(x)) for x in libraries]])
    results = await grafana.libraryelement.list_library_elements(folder_filter=libraries)
    return {x['name']: {'id': x['id'], 'uid': x['uid'], 'folderUid': x['folderUid']}
            for x in results['result']['elements']}


def pack_library_element(element_data):
    return {'gridPos': element_data['model']['gridPos'],
            'id': element_data['model']['id'],
            'title': element_data['model']['title'],
            'name': element_data['name'],
            'uid': element_data['uid']}


async def get_library_panel(name=None, uid=None, full=False):
    if name:
        result = await grafana.libraryelement.get_library_element_by_name(name)
    elif uid:
        result = await grafana.libraryelement.get_library_element(uid)
    else:
        raise AttributeError("Either name or uid needs to be provided.")
    if len(result['result']) != 1:
        raise ValueError(f"Expected to get a single result. Got {len(result['result'])}")
    if full:
        return result['result'][0]
    else:
        return pack_library_element(result['result'][0])
