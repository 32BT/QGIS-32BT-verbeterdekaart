

from qgis.core import *
from qgis.PyQt import uic
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtWidgets import QDialog

from ..pdok import WFS

################################################################################
### Settings Definitions
################################################################################
'''
QGIS.ini:

[32bt.verbeterdekaart]
vdk/services/selectie=BGT
vdk/services/BGT/filter/code='K0001'
'''

from ..qgs.settings import Settings


class Services(dict):
    NAME = 'selectie'
    def getSelectedServiceID(self):
        return self.get(self.NAME) or 'BGT'
    def setSelectedServiceID(self, _name):
        self[self.NAME] = _name
    def getService(self, _id=None):
        service = self.get(_id or self.getSelectedServiceID())
        return Service(service or {})
    def setService(self, _id, service):
        self[self.NAME] = _id
        self[_id] = service


class Service(dict):
    class TYPES:
        KEY = 'type'
        OGC = 'OGC'
        WFS = 'WFS'
    class FILTERS:
        KEY = 'filter'
        CODE = 'code'
    TYPE = TYPES.KEY

    def getType(self):
        return self.get(self.TYPE) or self.TYPES.WFS
    def setType(self, value):
        if not isinstance(value, str):
            value = (self.TYPES.WFS, self.TYPES.OGC)[bool(value)]
        self[self.TYPE] = value
        return value
    def getFilters(self):
        return self.get(self.FILTERS.KEY) or {}
    def setFilters(self, filters):
        self[self.FILTERS.KEY] = filters

    def getFilterString(self, _id='code'):
        return self.getFilters().get(_id) or ''
    def setFilterString(self, _id='code', filterStr=''):
        filters = self.getFilters()
        filters[_id] = filterStr
        self.setFilters(filters)


################################################################################
### Labels
################################################################################

import sys
_MODULE = sys.modules.get(__name__.split('.')[0])

_LABELS = _MODULE.LANGUAGE.LABELS({
    "SERVICEDIALOG_TITLE":
        "Terugmeldingen",

    "SERVICEDIALOG_SERVICEINFO":
        "Selecteer het gewenste type terugmeldingen.",

    "SERVICEDIALOG_SERVICELABEL":
        "Servicetype:",

    "SERVICEDIALOG_FILTERINFO":
        ["Voer optioneel een bronhoudercode in om",
        "meldingen via de service te filteren."],

    "SERVICEDIALOG_FILTERLABEL":
        "Bronhoudercode:"})

_LABELS.SERVICEDIALOG_FILTERINFO = '\n'.join(_LABELS.SERVICEDIALOG_FILTERINFO)

################################################################################
### .ui file
################################################################################

import os

def _form():
    path, ext = os.path.splitext(__file__)
    return uic.loadUiType(path+'.ui')[0]

################################################################################
### Dialog
################################################################################

class Dialog(QDialog, _form()):

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        # Ensure translated labels
        self.setWindowTitle(_LABELS.SERVICEDIALOG_TITLE)
        self.serviceInfo.setText(_LABELS.SERVICEDIALOG_SERVICEINFO)
        self.serviceLabel.setText(_LABELS.SERVICEDIALOG_SERVICELABEL)
        self.filterInfo.setText(_LABELS.SERVICEDIALOG_FILTERINFO)
        self.filterLabel.setText(_LABELS.SERVICEDIALOG_FILTERLABEL)

        self.serviceCombo.clear()
        self.serviceCombo.addItems(list(WFS.ENDPOINT.URL))
        self.serviceCombo.currentTextChanged.connect(self.serviceChanged)

        self._services = Settings.load_group(Services.__name__.lower()) or {}
        self._services = Services(self._services)


    def serviceChanged(self, selected):
        # Get service settings for selected service
        services = self._services
        service = services.getService(selected)
        ogctype = service.getType()==service.TYPES.OGC
        codestr = service.getFilterString()
        # Stuff UI controls
        self.serviceType.setChecked(ogctype)
        self.filterString.setText(codestr)

    ########################################################################
    ### Entrypoint
    ########################################################################

    def askInput(self):
        self.load()
        if self.exec():
            return self.save()

    def load(self):
        services = self._services
        selected = services.getSelectedServiceID()
        self.serviceCombo.setCurrentText(selected)
        self.serviceChanged(selected)

    def save(self):
        # Fetch UI controls
        _name = self.serviceCombo.currentText()
        _type = self.serviceType.isChecked()
        _code = self.filterString.text() or None
        # Update services settings
        services = self._services
        service = services.getService(_name)
        service.setType(_type)
        service.setFilterString(filterStr=_code)
        services.setService(_name, service)
        Settings.save_group(Services.__name__.lower(), services)
        _type = service.getType()
        return _name, _type, _code
