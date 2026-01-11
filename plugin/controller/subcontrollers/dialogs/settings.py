

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

    "SETTINGSDIALOG_MAINLABEL":
        ["Voer een percentage in om de schaal van",
        "verbeterdekaart aan te passen."],

    "SETTINGSDIALOG_SCALELABEL":
        "Schalingspercentage:"})

_LABELS.SETTINGSDIALOG_MAINLABEL = '\n'.join(_LABELS.SETTINGSDIALOG_MAINLABEL)

################################################################################
### Dialog
################################################################################

class Dialog(QDialog, _form()):

    def __init__(self, parent):
        super().__init__(parent)
        self.setupUi(self)
        # Ensure translated labels
        self.setWindowTitle(_LABELS.SETTINGSDIALOG_TITLE)
        self.mainLabel.setText(_LABELS.SETTINGSDIALOG_MAINLABEL)
        self.scaleLabel.setText(_LABELS.SETTINGSDIALOG_SCALELABEL)

    ########################################################################
    ### Entrypoint
    ########################################################################

    def askInput(self, settings):
        scaleValue = settings.get('schalingspercentage')
        self.setScale(scaleValue)
        if self.exec():
            scaleValue = self.getScale()
            settings['schalingspercentage'] = scaleValue
            return settings

    ########################################################################

    def getScale(self):
        return self.scaleValue.value()

    def setScale(self, value):
        self.scaleValue.setValue(int(value or 100))


    '''

    def __init__(self, parent):
        super().__init__(parent=parent)

        # setup dialog box items
        self.setWindowTitle(_LABELS.SETTINGSDIALOG_TITLE)
        self._label = QLabel(_LABELS.SETTINGSDIALOG_LABEL1)
        self._scaleLabel = QLabel(_LABELS.SETTINGSDIALOG_LABEL2)
        self._scaleValue = QSpinBox()
        self._scaleValue.setMinimum(1)
        self._scaleValue.setMaximum(500)
        self._scaleValue.setSingleStep(10)
        self._scaleValue.setStepType(\
            QAbstractSpinBox.StepType.AdaptiveDecimalStepType)
        self._scaleValue.setSuffix('%')
        self._scaleValue.setValue(100)

        buttons = QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        self._buttonBox = QDialogButtonBox(buttons)
        self._buttonBox.accepted.connect(self.accept)
        self._buttonBox.rejected.connect(self.reject)

        # layout dialog box items
        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self._label)
        layout = QHBoxLayout()
        layout.addWidget(self._scaleLabel)
        layout.addWidget(self._scaleValue, alignment=Qt.AlignLeft)
        layout.addStretch()
        layout.setContentsMargins(0,10,0,20)
        self.layout().addLayout(layout)

        self.layout().addWidget(self._buttonBox)
    '''
