
import os

from qgis.PyQt.QtGui import QIcon

def loadIcon(iconName):
    path = os.path.split(__file__)[0]
    path = os.path.join(path, iconName)
    path, ext = os.path.splitext(path)
    path += ext or '.svg'
    return QIcon(path)
