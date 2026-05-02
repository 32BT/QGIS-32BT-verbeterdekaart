

from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *

################################################################################
### MenuButton
################################################################################
'''
NOTE:
QToolButton does not unraise properly after showing the menu in instant mode.
In delayed mode, it works fine. The problem is in showMenu which probably
catches away mouse events from the original control.
'''

class MenuButton(QToolButton):
    instantActionTriggered = pyqtSignal(object)
    delayedActionTriggered = pyqtSignal(object)

    class POPUPMODE:
        INSTANT = QToolButton.ToolButtonPopupMode.InstantPopup
        DELAYED = QToolButton.ToolButtonPopupMode.DelayedPopup

    def __init__(self, toolBar, icon=QIcon(), menu=None):
        super().__init__()

        '''
        In INSTANT mode, the button action will be ignored.
        '''
        self._action = QAction(icon, "Open Webpagina")
        self._action.setObjectName("vdk:menuButtonAction")
        self._action.triggered.connect(self.menuButtonTriggered)

        self.setObjectName("vdk:menuButton")
        self.setPopupMode(self.POPUPMODE.INSTANT)
        self.setDefaultAction(self._action)
        toolBar.addWidget(self)

        self.setMenu(menu)
        menu.triggered.connect(self.menuActionTriggered)

    ########################################################################
    '''
    def setMenu(self, menu):
        _menu = self.menu()
        if _menu: _menu.aboutToShow.disconnect(self._aboutToShowMenu)
        _menu = menu
        if _menu: _menu.aboutToShow.connect(self._aboutToShowMenu)
        super().setMenu(menu)
    '''
    ########################################################################

    def setFocusMode(self, mode="Ad hoc"):
        self._action._targetPage = mode
        self.menu().prepare(mode)
        if mode in ('BAG', 'BGT', 'AERO'):
            self.setPopupMode(self.POPUPMODE.DELAYED)
            mode = self.menu().findModeTitle(mode)
            self._action.setText("Open "+mode)
        else:
            self.setPopupMode(self.POPUPMODE.INSTANT)
            self._action.setText("Open Menu...")

    def menuButtonTriggered(self, action=None):
        self.instantActionTriggered.emit(self._action)

    def menuActionTriggered(self, action=None):
        if self.popupMode() == self.POPUPMODE.INSTANT:
            self.instantActionTriggered.emit(action)
        else:
            self.delayedActionTriggered.emit(action)
