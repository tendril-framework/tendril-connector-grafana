from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

from .manager import AuthzDomainsManager
_manager = AuthzDomainsManager(prefix='tendril.authz.domains')

import sys
sys.modules[__name__] = _manager
_manager.finalize()
