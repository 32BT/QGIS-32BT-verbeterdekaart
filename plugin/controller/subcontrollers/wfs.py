

import os

from qgis.PyQt.QtGui import *
from qgis.core import *

from .dialogs import ServicesDialog
from . import pdok as PDOK

################################################################################
### WFSController
################################################################################

class Controller:

    def __init__(self, iface, toolBar):
        self._iface = iface

        action = QAction("Start WFS laag...")
        action.setIcon(self._loadIcon())
        action.setObjectName('vdk:startLayer')
        action.triggered.connect(self.startLayer)
        toolBar.addAction(action)

        self._action = action


    def _loadIcon(self, name="wfs"):
        path = os.path.split(__file__)[0]
        path = os.path.join(path, 'icons')
        path = os.path.join(path, name+'.svg')
        return QIcon(path)


    def startLayer(self):
        parent = self._iface.mainWindow()
        result = ServicesDialog(parent).askInput()
        if result is not None:
            serviceType, codeFilter = result
            url = PDOK.WFS.get_url(*result)
            print(url)
            layer = QgsVectorLayer(url, serviceType+' Terugmeldingen', 'WFS')
            QgsProject.instance().addMapLayer(layer)
