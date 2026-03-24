

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
    "SETTINGSDIALOG_TITLE":
        "Voorkeuren",

    "SETTINGSDIALOG_TARGETINFO":
        "Kies de verbeterdekaart landingspagina.",

    "SETTINGSDIALOG_TARGETNOTE":
        "n.b.: Deze optie is ook beschikbaar als je de werkbalk knop kortstondig ingedrukt houdt.",

    "SETTINGSDIALOG_TARGETLABEL":
        "Landingspagina:",

    "SETTINGSDIALOG_SCALEINFO":
        "Geef eventueel een weergaveschaling op.",

    "SETTINGSDIALOG_SCALENOTE":
        "De kaartweergave op de website wordt opgeroepen met dezelfde schaal als je werkblad. Er kunnen alsnog schalingsverschillen bestaan. Het schalingspercentage vergroot of verkleint de opgeroepen weergave.",

    "SETTINGSDIALOG_SCALELABEL":
        "Schalingspercentage:"})

################################################################################
### Dialog
################################################################################

class Dialog(QDialog, _form()):

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        # Ensure translated labels
        self.setWindowTitle(_LABELS.SETTINGSDIALOG_TITLE)
        self.targetInfo.setText(_LABELS.SETTINGSDIALOG_TARGETINFO)
        self.targetNote.setText(_LABELS.SETTINGSDIALOG_TARGETNOTE)
        self.targetLabel.setText(_LABELS.SETTINGSDIALOG_TARGETLABEL)
        self.scaleInfo.setText(_LABELS.SETTINGSDIALOG_SCALEINFO)
        self.scaleNote.setText(_LABELS.SETTINGSDIALOG_SCALENOTE)
        self.scaleLabel.setText(_LABELS.SETTINGSDIALOG_SCALELABEL)

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

