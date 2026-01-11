

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
        serviceType = service.get('type') or 'BGT'
        codeFilter = service.get('filter') or ''
        self.serviceCombo.setCurrentText(serviceType)
        self.codeFilter.setText(codeFilter)

    def saveSettings(self):
        serviceType = self.serviceCombo.currentText()
        codeFilter = self.codeFilter.text()
        service['type'] = serviceType
        service['filter'] = codeFilter
        Settings.save_group('service', service)
        return serviceType, codeFilter
