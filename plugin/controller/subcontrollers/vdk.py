

import math, webbrowser

import os

from qgis.gui import *
from qgis.core import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtWidgets import *
from qgis.PyQt.QtGui import *

from .dialogs import SettingsDialog
from .qgs.settings import Settings
from .qgs.mapcanvas import MapCanvas

from . import pdok as PDOK

from .icons import loadIcon
from .menu import MenuButton

################################################################################
### Contextmenu
################################################################################
'''
'''
import sys
_MODULE = sys.modules.get(__name__.split('.')[0])

_LABELS = _MODULE.LANGUAGE.LABELS({
    "CANVASMENU": {
        "TITLE": "verbeterdekaart",
        "ITEM1": "Voorkeuren..."
    }
})

################################################################################
### VDKController
################################################################################

class Controller:
    '''
    Hoofdmenu items behoeven geen vertaling.
    '''
    ITEM_LABEL1 = "BAG Viewer (BAG)"
    ITEM_LABEL2 = "Verbeter de Kaart (BGT/BRT/3DB)"
    ITEM_LABEL3 = "Verbeter de Luchtvaartkaart (AERO)"

    @classmethod
    def addTargetPageItems(cls, menu):
        action = menu.addAction(cls.ITEM_LABEL1)
        action._targetPage = 'BAG'
        action = menu.addAction(cls.ITEM_LABEL2)
        action._targetPage = 'BGT'
        action = menu.addAction(cls.ITEM_LABEL3)
        action._targetPage = 'AERO'
        return menu

    ########################################################################
    ### Voorkeuren
    ########################################################################
    class SETTINGS:
        GROUP = 'voorkeuren'
        SCALE = 'schalingspercentage'
        SOURCE = 'bron'
        TARGET = 'doel'

    def _loadSettings(self):
        return Settings.load_group(self.SETTINGS.GROUP)
    def _saveSettings(self, settings):
        Settings.save_group(self.SETTINGS.GROUP, settings)

    ########################################################################

    def __init__(self, iface, toolBar):
        self._iface = iface

        self._menuButton = MenuButton(toolBar, loadIcon("vdk"))
        menu = self._menuButton.getMenu()
        menu = self.addTargetPageItems(menu)
        menu.triggered.connect(self.startBrowser)

        self._canvasMenu = self.initCanvasMenu()
        self._mapCanvas = MapCanvas(self._iface.mapCanvas())
        self._mapCanvas.connectMenuHandler(self.prepareCanvasMenu)
        self._mapCanvas.connectExtentHandler(self.updateActions)

        self._settings = settings = self._loadSettings()
        self._scaleValue = int(settings.get(self.SETTINGS.SCALE) or 100)
        self._targetPage = settings.get(self.SETTINGS.TARGET) or 'BGT'

    def __del__(self):
        self._mapCanvas.disconnectExtentHandler(self.updateActions)
        self._mapCanvas.disconnectMenuHandler(self.prepareContextMenu)
        self._mapCanvas = None

    ########################################################################

    def updateActions(self):
        enable = self.isDomainVisible()
        self._menuButton.setEnabled(enable)

    def isDomainVisible(self):
        crs = QgsCoordinateReferenceSystem('EPSG:28992')
        mapR = self._mapCanvas.visibleExtent(crs)
        dstR = QgsRectangle(0, 300000, 300000, 630000)
        return mapR.intersects(dstR)

    ########################################################################
    ### Options
    ########################################################################
    '''
    def initButtonMenu(self):
        menu = QMenu("TargetService")
        menu = self.addTargetPageItems(menu)
        menu.triggered.connect(self.startBrowser)
        menu.aboutToShow.connect(self.buttonMenuAboutToShow)
        return menu

    def buttonMenuAboutToShow(self):
        self.updateButtonMenu()

    def buttonMenuAboutToHide(self):
        self._toolButton.setDown(False)

    def updateButtonMenu(self):
        icon0 = QIcon()
        icon1 = self._loadIcon('chk')
        for action in self._buttonMenu.actions():
            if action._targetPage != self._targetPage:
                action.setIcon(icon0)
            else:
                action.setIcon(icon1)
                self._buttonMenu.setDefaultAction(action)

    def setOption(self, action):
        self._targetPage = action._targetPage
        self._settings[self.SETTINGS.TARGET] = self._targetPage
        self._saveSettings(self._settings)
    '''
    ########################################################################
    ### Submenu
    ########################################################################

    def initCanvasMenu(self):
        menu = QMenu(_LABELS.CANVASMENU.TITLE)
        action = menu.addAction(_LABELS.CANVASMENU.ITEM1)
        action.triggered.connect(self.adjustSettings)
        menu.addSeparator()
        menu = self.addTargetPageItems(menu)
        menu.triggered.connect(self.startBrowser)
        return menu

    ########################################################################
    ### Contextmenu preparation
    ########################################################################
    '''
    The process is started by right-clicking the mapCanvas. This will present
    a contextmenu. Just before the contextmenu will be shown, a signal will be
    emitted: contextMenuAboutToShow. This signal allows us to append the menu
    with our submenu.

    The incoming menu starts out empty each time the signal is triggered.
    Following will add our "verbeterdekaart" menu with 3 submenus.
    '''
    def prepareCanvasMenu(self, menu, event):
        if self.isDomainVisible():
            if len(menu.actions()) == 1:
                menu.addSeparator()
            # Add submenu to context menu
            action = menu.addMenu(self._canvasMenu)

    ########################################################################
    ### Contextmenu actions
    ########################################################################
    '''
    If the user actually selects one of the menuitems, the corresponding
    action will be triggered.
        Action 1 will start a dialog to set preferences, specifically
            a compensation for verbeterdekaart scaling.
        Action 2 will copy the current maplocation & scale in
            verbeterdekaart-compatible format to the clipboard.
        Action 3 will open the current maplocation & scale in
            the default webbrowser.

    action slot definition:
        actionSlot([isChecked])
    '''
    # Action 1: adjust preferences
    def adjustSettings(self):
        parent = self._iface.mainWindow()
        settings = self._loadSettings()
        result = SettingsDialog(parent).askInput(settings)
        if result:
            self._saveSettings(result)
            self._targetPage = result.get(self.SETTINGS.TARGET)
            self._scaleValue = result.get(self.SETTINGS.SCALE) or 100

    # Action 2: Copy location
    def saveToClipboard(self):
        url = self._getURL(self._targetPage)
        clipBoard = QgsApplication.clipboard()
        clipBoard.setText(url)

    # Action 3: Open verbeterdekaart in default webbrowser
    def startBrowser(self, action=None):
        if hasattr(action, '_targetPage'):
            url = self._getURL(action._targetPage)
            QDesktopServices.openUrl(QUrl(url))
            #webbrowser.open(url)

    ########################################################################
    ### verbeterdekaart URL
    ########################################################################
    '''
    '''
    def _getURL(self, service='BAG', point=None, scale=None):
        # Fetch default values if necessary
        if point is None: point = self._mapCanvas.getCenter()
        if scale is None: scale = self._mapCanvas.getScale()

        # Compensate for CRS if necessary
        target_crs = PDOK.VDK.get_service_crs(service)
        target_crs = QgsCoordinateReferenceSystem(target_crs)
        point = self._mapCanvas.convertMapPoint(point, target_crs)
        # Compensate scalefactor for webbrowser-scale differences
        scale = scale * 100. / self._scaleValue

        return PDOK.VDK.get_service_url(service, point, scale)

################################################################################
