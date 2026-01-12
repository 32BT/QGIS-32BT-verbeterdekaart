

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

class _SETTINGS:
    NAME = 'services'
    TYPE = 'selectie'
    class FILTER:
        NAME = 'filter'
        CODE = 'code'

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

    "SERVICEDIALOG_OWNERINFO":
        ["Voer optioneel een bronhoudercode in om",
        "meldingen via de service te filteren."],

    "SERVICEDIALOG_SERVICELABEL":
        "Servicetype:",

    "SERVICEDIALOG_OWNERLABEL":
        "Bronhoudercode:"})

_LABELS.SERVICEDIALOG_OWNERINFO = '\n'.join(_LABELS.SERVICEDIALOG_OWNERINFO)

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
        self.ownerInfo.setText(_LABELS.SERVICEDIALOG_OWNERINFO)
        self.ownerLabel.setText(_LABELS.SERVICEDIALOG_OWNERLABEL)

        self.serviceCombo.addItems(list(WFS._URLS))
        self.serviceCombo.currentTextChanged.connect(self.serviceChanged)

        self._services = Settings.load_group(_SETTINGS.NAME) or {}


    def serviceChanged(self, selected):
        # Get service settings for selected service
        services = self._services
        service = services.get(selected) or {}
        filters = service.get(_SETTINGS.FILTER.NAME) or {}
        codestr = filters.get(_SETTINGS.FILTER.CODE) or ''
        # Stuff UI controls
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
        selected = services.get(_SETTINGS.TYPE) or 'BGT'
        self.serviceCombo.setCurrentText(selected)
        self.serviceChanged(selected)

    def save(self):
        # Fetch UI controls
        _type = self.serviceCombo.currentText()
        _code = self.filterString.text() or None
        # Update services settings
        services = self._services
        services[_SETTINGS.TYPE] = _type
        service = services.get(_type) or {}
        filters = service.get(_SETTINGS.FILTER.NAME) or {}
        filters[_SETTINGS.FILTER.CODE] = _code
        service[_SETTINGS.FILTER.NAME] = filters
        services[_type] = service
        print(services)
        Settings.save_group(_SETTINGS.NAME, services)
        return _type, _code
