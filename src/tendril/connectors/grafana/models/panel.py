

from tendril.connectors.grafana.actions.libraries import get_library_panel


class PanelSpecBase(object):
    height = None
    width = None
    x = None
    y = None
    id = None
    title = None
    library_panel_name = None

    @property
    def gridPos(self):
        return {
            'h': self.height,
            'w': self.width,
            'x': self.x,
            'y': self.y
        }


async def generate_panel(spec):
    panel = await get_library_panel(name=spec.library_panel_name)
    layout = panel['gridPos']
    layout_overrides = {k: v for k, v in spec.gridPos.items() if v is not None}
    layout.update(layout_overrides)
    return {
        'gridPos': layout,
        'id': spec.id or panel['id'],
        'title': spec.title or panel['title'],
        'libraryPanel': {
            'name': panel['name'],
            'uid': panel['uid'],
        }
    }
