

from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *

################################################################################
### MenuButton
################################################################################

class MenuButton:

    def __init__(self, toolBar, icon=QIcon()):
        '''
        QToolButton with menu does not unraise properly after showing the menu,
        plus the tiny disclosure triangle is not particularely helpful for
        indicating a major InstantPopup.
        So we just build a full actionchain ourselves.
        '''
        self._menu = QMenu()
        self._menu.setObjectName("vdk:openBrowserMenu")
        self._menu.aboutToHide.connect(self.menuDidFinish)

        self._action = QAction()
        self._action.setObjectName("vdk:openBrowserAction")
        self._action.setIcon(icon)
        self._action.setText(self._menu.title())
        self._action.triggered.connect(self.showMenu)

        self._button = QToolButton()
        self._button.setObjectName("vdk:openBrowserButton")
        self._button.setDefaultAction(self._action)
        toolBar.addWidget(self._button)

    ########################################################################

    def setEnabled(self, enable=True):
        self._button.setEnabled(enable)

    def getButton(self):
        return self._button

    def getMenu(self):
        return self._menu

    def getAction(self):
        return self._action


    ########################################################################

    def showMenu(self, action):
        button = self._button
        button.setDown(True)
        x, y = 0, button.frameSize().height()
        self._menu.popup(button.mapToGlobal(QPoint(x,y)))
        return True

    def menuDidFinish(self):
        self._button.setDown(False)

