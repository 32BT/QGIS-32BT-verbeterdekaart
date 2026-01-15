

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
            _name, _type, _code = result
            if _type == False:
                url = self.get_uri_wfs(_name, _code)
                layer = QgsVectorLayer(url, _name+' Terugmeldingen', 'WFS')
            else:
                uri = self.get_uri_ogc(_name, _code)
                layer = QgsVectorLayer(uri, _name+' Terugmeldingen', 'oapif')

            self.setStyle(layer, 'BGT')
            QgsProject.instance().addMapLayer(layer)

    ########################################################################
    def get_uri_wfs(self, serviceName, codeFilter=''):
        url = PDOK.WFS.get_url(serviceName)
        prm = dict(url=url,
            srsname="EPSG:28992",
            typename="bgtterugmeldingen",
            restrictToRequestBBOX="1",
            pagingEnabled="enabled",
            pageSize="500",
            maxNumFeatures="10000")

        if codeFilter:
            codeFilter = self.getPostFilter(codeFilter) or codeFilter
            filter = "\"bronhoudercode\" LIKE '{}'".format(codeFilter)
            prm['filter'] = filter

        return self.getURI(prm)


    def get_uri_ogc(self, serviceName, codeFilter=''):
        postFilter = self.getPostFilter(codeFilter)
        if postFilter: codeFilter = None

        url = PDOK.OGC.get_url(serviceName, codeFilter)
        prm = dict(url=url,
            #crs="http://www.opengis.net/def/crs/EPSG/0/28992",
            srsname="EPSG:28992",
            #preferCoordinatesForWfsT11="false",
            typename="bgtterugmeldingen",
            restrictToRequestBBOX="1",
            pagingEnabled="enabled",
            pageSize="500",
            maxNumFeatures="10000")
        #prm['bbox-crs'] = "http://www.opengis.net/def/crs/EPSG/0/28992"

        if postFilter:
            filter = "\"bronhoudercode\" LIKE '{}'".format(postFilter)
            prm['filter'] = filter

        return self.getURI(prm)


    def getPostFilter(self, filterStr):
        if filterStr:
            if set(filterStr)&set('*%?_'):
                filterStr = filterStr.replace('*', '%')
                filterStr = filterStr.replace('?', '_')
                return filterStr

    def getURI(self, prm):
        uri = QgsDataSourceUri()
        for k,v in prm.items():
            uri.setParam(k, v)
        return uri.uri()

    ########################################################################

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

