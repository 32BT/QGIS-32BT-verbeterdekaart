

################################################################################
### Plugin Main
################################################################################
'''
'''

from .controller import ToolBar
from .controller import Controller

class Plugin:
    def __init__(self, iface):
        self._iface = iface

    def initGui(self):
        self._toolBar = ToolBar(self._iface)
        self._controller = Controller(self._iface, self._toolBar)

    def unload(self):
        self._controller = None
        self._toolBar = None

################################################################################
