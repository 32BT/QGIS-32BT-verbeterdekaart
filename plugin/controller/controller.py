



import sys
_MODULE = sys.modules.get(__name__.split('.')[0])
_IDENTITY = _MODULE.IDENTITY
_LANGUAGE = _MODULE.LANGUAGE
_LABELS = _LANGUAGE.LABELS()

################################################################################
### Toolbar
################################################################################

class ToolBar:
    _NAME = _LABELS.TOOLBAR_TITLE
    _GUID = _IDENTITY.PREFIX+"Toolbar"

    def __new__(cls, iface):
        toolBar = iface.addToolBar(cls._NAME)
        toolBar.setObjectName(cls._GUID)
        return toolBar

################################################################################
### Controller
################################################################################

from .subcontrollers import VDKController
from .subcontrollers import WFSController

class Controller:

    def __init__(self, iface, toolBar):
        self._iface = iface
        self._Wfs = WFSController(iface, toolBar)
        self._vdk = VDKController(iface, toolBar)

################################################################################
