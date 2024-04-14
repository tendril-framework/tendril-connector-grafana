# Copyright (C) 2019 Chintalagiri Shashank
#
# This file is part of Tendril.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
Grafana Configuration Options
==============================
"""


from tendril.utils.config import ConfigOption
from tendril.utils import log
logger = log.get_logger(__name__, log.DEFAULT)

depends = ['tendril.config.core']


config_elements_grafana = [
    ConfigOption(
        'GRAFANA_SERVER_HOST',
        "'localhost'",
        "Grafana Server Host"
    ),
    ConfigOption(
        'GRAFANA_SERVER_PORT',
        "3000",
        "Grafana Server Port"
    ),
    ConfigOption(
        'GRAFANA_SERVER_SSL',
        "True",
        "Whether to use SSL (https)."
    ),
    ConfigOption(
        'GRAFANA_BASE_URL',
        "''",
        "Base URL to use for Grafana Embed Links. This is technically the same as the "
        "server pointed to by GRAFANA_SERVER-*, but must be spearately configured for quirky "
        "reasons related to deployment topologies."
    ),
    ConfigOption(
        'GRAFANA_ORG',
        "1",
        "Grafana Organization to use. This is normally 1, unless the Grafana is multi-tenant. "
        "What should happen if Tendril itself is multi-tenant is unclear."
    ),
    ConfigOption(
        'GRAFANA_ADMIN_USER',
        "'admin'",
        "User to use with Grafana Admin API interfaces needing Basic Auth."
    ),
ConfigOption(
        'GRAFANA_ADMIN_PASSWORD',
        "'admin'",
        "Password to use with Grafana Admin API interfaces needing Basic Auth.",
        masked=True
    ),
    ConfigOption(
        'GRAFANA_PROVISIONER_TOKEN',
        "''",
        "Grafana Service Account token which allows creation and management of "
        "Teams and dashboards",
        masked=True
    ),
    # TODO We're using team composition for folders as well as teams. Improve the implementation
    #  to allow independent control.
    ConfigOption(
        'GRAFANA_TEAM_COMPOSITION',
        default="[]",
        doc="Tendril Interest Types which should be associated with Grafana Teams. "
            "Choose this to limit the number of teams to something reasonable while providing "
            "the needed isolation. Actual scaling characteristics of Grafana are not investigated. "
            "Values are expected to be tuples of form (type_name, include_children). "
            "'include_children' determines whether members in descendant "
            "interests get Team membership. "
            "  - 'True' gives access to all descendant children members. (implemented) "
            "  - (not implemented) List of tuples of type (type_name, include) gives access to "
            "     children of the specified type, and include can be similarly boolean or a list of Roles "
            "Members of limited children never get access. "
            "Members of ancestor interests always get access. "
    ),
    ConfigOption(
        'GRAFANA_TEAM_EMAIL_DOMAIN',
        default='.tendril.link',
        doc="Domain suffix to use for team emails. This is not particularly "
            "important, it just is."
    ),
    ConfigOption(
        'GRAFANA_DATASOURCE_INFLUXDB_MONITORS',
        default='None',
        doc="InfluxDB datasource to use for Grafana for Tendril Monitors. This should be separately be "
            "configured and prepared, and only the Name should be provided here."
    ),
    ConfigOption(
        'GRAFANA_DATASOURCE_BACKEND_READER',
        default='None',
        doc="PostgreSQL datasource to use for Grafana for Tendril Backend Read. This should be "
            "separately be configured and prepared, and only the Name should be provided here. "
            "Typically, this would be a user on the primary database with Read Only access. "
            "Currently, we only use the Interest table."
    ),
    ConfigOption(
        'GRAFANA_LIBRARIES_FOLDER',
        default='"Library"',
        doc="Top level folder for Grafana Library panels. Generally, users are expected to have full "
            "read acces to this folder and everything beneath this. The actual folder structure within "
            "is somewhat implementation / instance dependent. Presently, we are implementing for folders "
            "to have the lowercase singular name of the interest type they apply to."
    ),
]


def load(manager):
    logger.debug("Loading {0}".format(__name__))
    manager.load_elements(config_elements_grafana,
                          doc="Tendril Grafana Configuration")
