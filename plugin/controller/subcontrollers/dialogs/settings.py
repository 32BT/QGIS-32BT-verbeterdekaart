

from qgis.core import *
from qgis.PyQt import uic
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtWidgets import QDialog


################################################################################

import os

def _form():
    path, ext = os.path.splitext(__file__)
    form, _ = uic.loadUiType(path+'.ui')
    return form

################################################################################
### Labels
################################################################################

_LABELS = {
    "SETTINGSDIALOG": {
        "TITLE": "Voorkeuren",

        "TARGET": {
            "TITLE": "Werkbalk knop",
            "NOTE": "Kies een doelmodus voor de werkbalk knop.",
            "LABEL": "Doelmodus:",
            "INFO":
                "Ad hoc modus toont altijd een keuzemenu voor de landingspagina.\nFocus modus opent direct de voorgeselecteerde pagina. (Je kunt de voorselectie wisselen door de knop even ingedrukt te houden.)"
        },

        "SCALE": {
            "TITLE": "Website weergave",
            "NOTE": "Geef eventueel een weergaveschaling op.",
            "LABEL": "Schalingspercentage:",
            "INFO":
                "De kaartweergave op de website wordt opgeroepen met dezelfde schaal als je werkblad. Er kunnen alsnog schalingsverschillen bestaan. Deze waarde vergroot of verkleint de opgeroepen weergave."
        }
    }
}

import sys
_MODULE = sys.modules.get(__name__.split('.')[0])
_LABELS = _MODULE.LANGUAGE.LABELS(_LABELS)
_LABELS = _LABELS.SETTINGSDIALOG

################################################################################
### Dialog
################################################################################

class Dialog(QDialog, _form()):

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        # Ensure translated labels
        self.setWindowTitle(_LABELS.TITLE)
        self.targetGroup.setTitle(_LABELS.TARGET.TITLE)
        self.targetNote.setText(_LABELS.TARGET.NOTE)
        self.targetLabel.setText(_LABELS.TARGET.LABEL)
        self.targetInfo.setText(_LABELS.TARGET.INFO)
        self.scaleGroup.setTitle(_LABELS.SCALE.TITLE)
        self.scaleNote.setText(_LABELS.SCALE.NOTE)
        self.scaleLabel.setText(_LABELS.SCALE.LABEL)
        self.scaleInfo.setText(_LABELS.SCALE.INFO)

        self.targetMenu.insertSeparator(1)

    ########################################################################
    ### Entrypoint
    ########################################################################

    def askInput(self, settings):
        self.setTarget(settings.get_targetMode())
        self.setScale(settings.get_scaleValue())
        if self.exec():
            settings.set_targetMode(self.getTarget())
            settings.set_scaleValue(self.getScale())
            return settings

    ########################################################################

    def getTarget(self):
        return self.targetMenu.currentText()

    def setTarget(self, value):
        self.targetMenu.setCurrentText(value)


    def getScale(self):
        return self.scaleValue.value()

    def setScale(self, value):
        self.scaleValue.setValue(int(value or 100))

