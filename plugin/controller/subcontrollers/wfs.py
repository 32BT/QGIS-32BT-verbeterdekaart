

import os

from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
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
            self.setStyle(layer, 'BGT')
            QgsProject.instance().addMapLayer(layer)


    def setStyle(self, layer, name='BGT'):
        path = os.path.split(__file__)[0]
        path = os.path.join(path, 'qml')
        path = os.path.join(path, name.lower()+'.qml')
        if os.path.exists(path):
            layer.loadNamedStyle(path,
                flags=Qgis.LoadStyleFlag.IgnoreMissingStyleErrors)
        else:
            symbol = layer.renderer().symbol()
            symbol.setColor(QColor.fromRgb(255,255,0))

