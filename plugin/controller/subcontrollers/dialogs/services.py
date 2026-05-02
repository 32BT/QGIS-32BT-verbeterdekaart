

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
    class SELECTION:
        KEY = 'selectie'
    class STYLING:
        KEY = 'stijl'
        class OPTION:
            STANDARD = 'standaard'
            SHORT = 'kort'
            CUSTOM = 'aangepast'
            LIST = (STANDARD, SHORT, CUSTOM)

    def getSelectedServiceID(self):
        return self.get(self.SELECTION.KEY) or 'BGT'
    def setSelectedServiceID(self, _name):
        self[self.SELECTION.KEY] = _name

    def getStyling(self):
        return self.get(self.STYLING.KEY) or self.STYLING.OPTION.STANDARD
    def setStyling(self, value):
        self[self.STYLING.KEY] = value

    def getService(self, _id=None):
        service = self.get(_id or self.getSelectedServiceID())
        return Service(service or {})
    def setService(self, _id, service):
        self[self.SELECTION.KEY] = _id
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

_LABELS = {
    "SERVICEDIALOG": {
        "TITLE": "Terugmeldingen",
        "SERVICE": {
            "INFO": "Selecteer het gewenste type terugmeldingen.",
            "LABEL": "Servicetype: "
        },
        "FILTER": {
            "INFO":
                ["Voer optioneel een bronhoudercode in om",
                "meldingen via de service te filteren."],
            "LABEL": "Bronhoudercode: "
        },
        "STYLING": {
            "NOTE": "Status indicatie",
            "OPTION1": "Standaard",
            "OPTION2": "Kort",
            "OPTION3": "Aangepast"
        }
    }
}


import sys
_MODULE = sys.modules.get(__name__.split('.')[0])
_LABELS = _MODULE.LANGUAGE.LABELS(_LABELS)

_LABELS.SERVICEDIALOG.FILTER.INFO = '\n'.join(_LABELS.SERVICEDIALOG.FILTER.INFO)

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
        self.setWindowTitle(_LABELS.SERVICEDIALOG.TITLE)
        self.serviceInfo.setText(_LABELS.SERVICEDIALOG.SERVICE.INFO)
        self.serviceLabel.setText(_LABELS.SERVICEDIALOG.SERVICE.LABEL)
        self.filterInfo.setText(_LABELS.SERVICEDIALOG.FILTER.INFO)
        self.filterLabel.setText(_LABELS.SERVICEDIALOG.FILTER.LABEL)
        self.stylingNote.setText(_LABELS.SERVICEDIALOG.STYLING.NOTE)
        self.stylingOption1.setText(_LABELS.SERVICEDIALOG.STYLING.OPTION1)
        self.stylingOption2.setText(_LABELS.SERVICEDIALOG.STYLING.OPTION2)
        self.stylingOption3.setText(_LABELS.SERVICEDIALOG.STYLING.OPTION3)

        self.serviceCombo.clear()
        self.serviceCombo.addItems(list(WFS.ENDPOINT.URL))
        self.serviceCombo.currentTextChanged.connect(self.serviceChanged)

        self.stylingOption = {
            Services.STYLING.OPTION.STANDARD: self.stylingOption1,
            Services.STYLING.OPTION.SHORT:    self.stylingOption2,
            Services.STYLING.OPTION.CUSTOM:   self.stylingOption3
        }

        self._services = Settings.load_group(Services.__name__.lower()) or {}
        self._services = Services(self._services)


    def serviceChanged(self, selected):
        # Get service settings for selected service
        services = self._services
        service = services.getService(selected)
        ogctype = service.getType()==service.TYPES.OGC
        codestr = service.getFilterString()
        styling = services.getStyling()
        # Stuff UI controls
        self.serviceType.setChecked(ogctype)
        self.filterString.setText(codestr)
        self.stylingOption.get(styling).setChecked(True)

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
        _mode = self.getStylingOption()
        # Update services settings
        services = self._services
        service = services.getService(_name)
        service.setType(_type)
        service.setFilterString(filterStr=_code)
        services.setStyling(_mode)
        services.setService(_name, service)
        Settings.save_group(Services.__name__.lower(), services)
        _type = service.getType()
        return _name, _type, _code, _mode

    def getStylingOption(self):
        for k, v in self.stylingOption.items():
            if v.isChecked(): return k
