

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
catches mouse events away from the original control.
'''

class MenuButton(QToolButton):
    class POPUP:
        INSTANT = QToolButton.ToolButtonPopupMode.InstantPopup
        DELAYED = QToolButton.ToolButtonPopupMode.DelayedPopup

    def __init__(self, toolBar, icon=QIcon(), menu=None):
        super().__init__()

        '''
        In INSTANT mode, the action will be ignored.
        '''
        self._action = QAction(icon, "Open Webpagina")
        self._action.setObjectName("vdk:menuButtonAction")
        self._action.triggered.connect(self.startBrowser)

        self.setObjectName("vdk:menuButton")
        self.setPopupMode(self.POPUP.INSTANT)
        self.setDefaultAction(self._action)
        toolBar.addWidget(self)

        self.setMenu(menu)

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
        self._focusMode = mode
        self.menu().prepare(mode)
        if mode in ('BAG', 'BGT', 'AERO'):
            self.setPopupMode(self.POPUP.DELAYED)
        else:
            self.setPopupMode(self.POPUP.INSTANT)

    def startBrowser(self, action=None):
        print('startBrowser')
