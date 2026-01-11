

from qgis.core import *
from qgis.PyQt import uic
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtWidgets import QDialog


from ..pdok import WFS
from ..qgs.settings import Settings

################################################################################

import os

def _form():
    path, ext = os.path.splitext(__file__)
    form, _ = uic.loadUiType(path+'.ui')
    return form

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

    ########################################################################
    ### Entrypoint
    ########################################################################

    def askInput(self):
        self.loadSettings()
        if self.exec():
            return self.saveSettings()

    def loadSettings(self):
        service = Settings.load_group('service')
        _type = service.get('type') or 'BGT'
        _code = service.get('code') or ''
        self.serviceCombo.setCurrentText(_type)
        self.filterString.setText(_code)

    def saveSettings(self):
        _type = self.serviceCombo.currentText()
        _code = self.filterString.text()
        service = dict(
            type = _type,
            code = _code)
        Settings.save_group('service', service)
        return _type, _code
