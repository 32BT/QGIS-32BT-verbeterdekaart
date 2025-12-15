
from qgis.gui import *
from qgis.core import *

################################################################################
### QgsMapCanvas controller
################################################################################
'''
MapCanvas is a wrapperobject for QgsMapCanvas with some helperfunctions for
readability and ease of access.
'''

class MapCanvas:

    def __init__(self, mapCanvas):
        self._mapCanvas = mapCanvas

    ########################################################################

    def connectMenuHandler(self, proc):
        self._mapCanvas.contextMenuAboutToShow.connect(proc)

    def disconnectMenuHandler(self, proc):
        self._mapCanvas.contextMenuAboutToShow.disconnect(proc)

    ########################################################################

    # Viewpoint for mapCanvas
    def getViewPoint(self):
        p = self._mapCanvas.center()
        s = self._mapCanvas.scale()
        return p, s

    def getCenter(self):
        return self._mapCanvas.center()

    def getScale(self):
        return self._mapCanvas.scale()

    # mappoint for mouseposition
    def getMapPointForEventPosition(self, eventPosition):
        # Translate eventPosition to mapPoint
        mapTransform = self._mapCanvas.getCoordinateTransform()
        return mapTransform.toMapCoordinates(eventPosition)

    # convert point from map crs to desired crs
    def convertMapPoint(self, mapPoint, crs):
        if crs and crs != self.getCrs():
            T = QgsCoordinateTransform(
                self.getCrs(), crs, QgsProject.instance())
            mapPoint = T.transform(mapPoint)
        return mapPoint

    def getCrs(self):
        return self._mapCanvas.mapSettings().destinationCrs()

    def getWidgetSize(self):
        size = self._mapCanvas.size()
        return size.width(), size.height()

################################################################################
