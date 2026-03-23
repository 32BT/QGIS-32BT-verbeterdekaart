

import os

from qgis.core import Qgis
from qgis.PyQt.QtGui import QColor

def loadStyle(layer, uid='BGT'):
    # brt.qml includes status=Geparkeerd
    name = ('bgt.qml', 'brt.qml')[uid in ('BRT', 'AERO')]
    path = os.path.split(__file__)[0]
    path = os.path.join(path, name)
    if os.path.exists(path):
        layer.loadNamedStyle(path,
            flags=Qgis.LoadStyleFlag.IgnoreMissingStyleErrors)
    else:
        symbol = layer.renderer().symbol()
        symbol.setColor(QColor.fromRgb(255,255,0))
