

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

import sys
_MODULE = sys.modules.get(__name__.split('.')[0])

_LABELS = _MODULE.LANGUAGE.LABELS({
    "SETTINGSDIALOG": {
        "TITLE":
            "Voorkeuren",

        "TARGET": {
            "NOTE":
                "Kies de verbeterdekaart landingspagina modus.",

            "INFO":
                "Ad-hoc modus toont altijd een keuzemenu.\nFocus modus gaat direct naar de gekozen landingspagina.\n(Je kunt alsnog wisselen door de werkbalkknop kortstondig \ningedrukt te houden.)",

            "LABEL":
                "Landingspagina:",
        },

        "SCALE": {
            "NOTE":
                "Geef eventueel een weergaveschaling op.",

            "INFO":
                "De kaartweergave op de website wordt opgeroepen met dezelfde schaal als je werkblad. Er kunnen alsnog schalingsverschillen bestaan. Het schalingspercentage vergroot of verkleint de opgeroepen weergave.",

            "LABEL":
                "Schalingspercentage:"
        }
    }
})

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
        self.targetNote.setText(_LABELS.TARGET.NOTE)
        self.targetLabel.setText(_LABELS.TARGET.LABEL)
        self.targetInfo.setText(_LABELS.TARGET.INFO)
        self.scaleNote.setText(_LABELS.SCALE.NOTE)
        self.scaleLabel.setText(_LABELS.SCALE.LABEL)
        self.scaleInfo.setText(_LABELS.SCALE.INFO)

        self.targetMenu.insertSeparator(1)

    ########################################################################
    ### Entrypoint
    ########################################################################

    def askInput(self, settings):
        self.setTarget(settings.get('doel'))
        self.setScale(settings.get('schalingspercentage'))
        if self.exec():
            settings['doel'] = self.getTarget()
            settings['schalingspercentage'] = self.getScale()
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

