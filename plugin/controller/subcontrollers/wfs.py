

import os

from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from qgis.core import *

from .dialogs import ServicesDialog
from . import pdok as PDOK


_WFS_EXP = '''
left("tijdstipRegistratie", 10) +': '+ "meldingsnummerVolledig" +'\n'+ trim("omschrijving") + coalesce('\nTOELICHTING: '+trim("toelichting"), '')
'''

_OGC_EXP = '''
format_date("tijdstip_registratie", 'yyyy-MM-dd') +': '+ "meldingsnummer_volledig" +'\n'+ trim("omschrijving") + coalesce('\nTOELICHTING: '+trim("toelichting"), '')
'''

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
        prm = dict(version='auto',
            url=PDOK.WFS.ENDPOINT(serviceName),
            typename=PDOK.WFS.ITEMTYPE(serviceName),
            srsname=PDOK.WFS.DEFAULT.CRS.NAME,
            restrictToRequestBBOX="1",
            pagingEnabled="enabled",
            pageSize="500",
            maxNumFeatures="10000")

        if codeFilter:
            # Replace * and ? for * and _
            codeFilter = self.getPostFilter(codeFilter) or codeFilter
            key, val = '"bronhoudercode"', "'{}'".format(codeFilter)
            prm['filter'] = key + " LIKE " + val

        return self.getURI(prm)

    '''
    The OGC filter parameters are not standard filter parameters.
    They currently are fixed parameters in the url. They do not allow wildcards.
    '''
    def get_uri_ogc(self, serviceName, codeFilter=''):
        # Wildcards are filtered in-app after download
        # codeFilter will be cleared and replaced by a postFilter,
        # if codeFilter contains one of *?_
        postFilter = self.getPostFilter(codeFilter)
        if postFilter: codeFilter = None

        url = PDOK.OGC.get_url(serviceName, codeFilter)
        prm = dict(url=url,
            srsname="EPSG:28992",
            typename="bgtterugmeldingen",
            restrictToRequestBBOX="1",
            pagingEnabled="enabled",
            pageSize="500",
            maxNumFeatures="10000")

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

