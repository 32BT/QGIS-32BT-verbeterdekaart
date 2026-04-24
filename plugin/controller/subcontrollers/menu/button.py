

from qgis.PyQt.QtCore import *
from qgis.PyQt.QtGui import *
from qgis.PyQt.QtWidgets import *

################################################################################
### MenuButton
################################################################################
'''
NOTE: QToolButton with menu does not unraise properly after showing the menu.
We therefore build an alternative button
'''

class MenuButton:

    def __init__(self, toolBar, icon=QIcon(), menu=None):

        self._action = QAction()
        self._action.setObjectName("vdk:menuButtonAction")
        self._action.setIcon(icon)
        self._action.setText("Open Webpagina")
        self._action.triggered.connect(self.showMenu)

        self._button = QToolButton()
        self._button.setObjectName("vdk:menuButton")
        self._button.setDefaultAction(self._action)
        toolBar.addWidget(self._button)

        self._menu = None
        self.setMenu(menu)

    ########################################################################

    def getMenu(self):
        return self._menu

    def setMenu(self, menu):
        if self._menu != menu:
            if self._menu: self._menu.aboutToHide.disconnect(self.menuDidFinish)
            self._menu = menu
            if self._menu: self._menu.aboutToHide.connect(self.menuDidFinish)

    ########################################################################

    def setEnabled(self, enable=True):
        self._button.setEnabled(enable)

    def showMenu(self, action):
        button = self._button
        button.setDown(True)
        x, y = 0, button.frameSize().height()
        self._menu.popup(button.mapToGlobal(QPoint(x,y)))
        return True

    def menuDidFinish(self):
        self._button.setDown(False)

