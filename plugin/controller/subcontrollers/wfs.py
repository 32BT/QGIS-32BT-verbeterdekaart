

import os

from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *
from qgis.core import *

from .icons import loadIcon
from .dialogs import ServicesDialog
from . import pdok as PDOK

################################################################################
### Label Expressions
################################################################################
'''
Separate label-expressions.
The label expression can be stated as a single expression applicable to both
WFS and OGC vars, but that just slows down labels unnecessarily.
'''
'''
def _EXP_KEY(key): return f'"{key}"'
date = _EXP_KEY("tijdstipRegistratie")
name = _EXP_KEY("meldingsnummerVolledig")
text = _EXP_KEY("omschrijving")
info = _EXP_KEY("toelichting")

_WFS_EXP = f"left({date}, 10)"
_WFS_EXP += f"+': '+{name}+'\\n'"
_WFS_EXP += f"+trim({text})"
_WFS_EXP += f"+coalesce('\\nTOELICHTING: '+trim({info}), '')"



date = _EXP_KEY("tijdstip_registratie")
name = _EXP_KEY("meldingsnummer_volledig")

_OGC_EXP = f"format_date({date}, 'yyyy-MM-dd')"
_OGC_EXP += f"+': '+{name}+'\\n'"
_OGC_EXP += f"+trim({text})"
_OGC_EXP += f"+coalesce('\\nTOELICHTING: '+trim({info}), '')"

'''


class LabelExpression:
    def __init__(self, layer):
        self._layer = layer
        self._fldNames = [f.name() for f in layer.fields()]
        self._keyNames = [name.lower().replace('_','') for name in self._fldNames]

    def getKey(self, key):
        try:
            i = self._keyNames.index(key.lower())
            key = self._fldNames[i]
        except ValueError: pass
        return f'"{key}"'

    def get(self, type='wfs'):
        date = self.getKey("tijdstipRegistratie")
        name = self.getKey("meldingsnummerVolledig")
        text = self.getKey("omschrijving")
        info = self.getKey("toelichting")

        exp = []
        if date:
            if type=='ogc':
                exp.append(f"format_date({date}, 'yyyy-MM-dd')")
            else:
                exp.append(f"left({date}, 10)")
            exp.append("': '")
        if name: exp.append(f"{name}+'\\n'")
        if text: exp.append(f"trim({text})")
        if info: exp.append(f"coalesce('\\nTOELICHTING: '+trim({info}), '')")
        return "+".join(exp)


def _set_label_expression(layer, exp):
    lab = layer.labeling()
    pal = lab.settings()
    pal.fieldName=exp
    pal.isExpression=True
    lab.setSettings(pal)

################################################################################
### WFSController
################################################################################

class Controller:

    def __init__(self, iface, toolBar):
        self._iface = iface
        self._action = self.initAction()
        toolBar.addAction(self._action)

    def initAction(self):
        action = QAction("Start WFS laag...")
        action.setIcon(loadIcon("wfs"))
        action.setObjectName("vdk:startLayer")
        action.triggered.connect(self.startLayer)
        return action


    def startLayer(self):
        parent = self._iface.mainWindow()
        result = ServicesDialog(parent).askInput()
        if result is not None:
            _name, _type, _code = result
            if _type == False:
                uri = self.get_wfs_uri(_name, _code)
                src = 'WFS'
                exp = 'wfs'
            else:
                uri = self.get_ogc_uri(_name, _code)
                src = 'oapif'
                exp = 'ogc'

            layer = QgsVectorLayer(uri, _name+' Terugmeldingen', src)
            self.setStyle(layer, _name)
            exp = LabelExpression(layer).get(exp)
            _set_label_expression(layer, exp)
            QgsProject.instance().addMapLayer(layer)

    ########################################################################
    ### WFS URI
    ########################################################################
    def get_wfs_uri(self, serviceName, codeFilter=''):
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

    ########################################################################
    ### OGC URI
    ########################################################################
    '''
    The OGC filter parameters are not standard filter parameters.
    They currently are fixed parameters in the url. They do not allow wildcards.
    Wildcardfilters are applied in-app after download.
    If the codeFilter contains a wildcard, the codeFilter will be cleared and
    replaced by postFilter.
    '''
    def get_ogc_uri(self, serviceName, codeFilter=''):
        postFilter = self.getPostFilter(codeFilter)
        if postFilter: codeFilter = None

        prm = dict(
            url=PDOK.OGC.ENDPOINT(serviceName),
            typename=PDOK.OGC.ITEMTYPE(serviceName),
            srsname=PDOK.OGC.DEFAULT.CRS.NAME,
            restrictToRequestBBOX="1",
            pagingEnabled="enabled",
            pageSize="500",
            maxNumFeatures="10000")

        if codeFilter:
            prm['url'] += f"?bronhoudercode={codeFilter}"
        if postFilter:
            prm['filter'] = f"\"bronhoudercode\" LIKE '{postFilter}'"

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

    def setStyle(self, layer, uid='BGT'):
        name = ('bgt.qml', 'brt.qml')[uid in ('BRT', 'AERO')]
        path = os.path.split(__file__)[0]
        path = os.path.join(path, 'qml')
        path = os.path.join(path, name)
        if os.path.exists(path):
            layer.loadNamedStyle(path,
                flags=Qgis.LoadStyleFlag.IgnoreMissingStyleErrors)
        else:
            symbol = layer.renderer().symbol()
            symbol.setColor(QColor.fromRgb(255,255,0))

