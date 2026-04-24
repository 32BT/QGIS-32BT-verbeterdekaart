

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
from .menu import TargetMenu


################################################################################
### VDKController
################################################################################

class Controller:

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

        self._menu = TargetMenu()
        self._menu.setObjectName("vdk:targetMenu")
        self._menu.triggered.connect(self.menuTriggered)

        self._menuButton = MenuButton(toolBar, loadIcon("vdk"))
        self._menuButton.setMenu(self._menu)

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
    '''
    Verbeterdekaart heeft alleen betekenis binnen Nederland.
    Als het werkblad niet overlapt met Nederland, dan worden
    de knoppen grijs, en is het canvasmenu niet beschikbaar.
    '''
    def updateActions(self):
        enable = self.isDomainVisible()
        self._menuButton.setEnabled(enable)

    def isDomainVisible(self):
        crs = QgsCoordinateReferenceSystem('EPSG:28992')
        mapR = self._mapCanvas.visibleExtent(crs)
        dstR = QgsRectangle(0, 300000, 300000, 630000)
        return mapR.intersects(dstR)

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
            action = menu.addMenu(self._menu)

    ########################################################################
    ### Menu actions
    ########################################################################
    '''
    If a menuaction is triggered, it will be either a verbeterdekaart target,
    or the settings options.
    '''
    def menuTriggered(self, action=None):
        target = getattr(action, '_targetPage', None)
        if target in PDOK.VDK.TARGET.LIST:
            url = self._getURL(target)
            QDesktopServices.openUrl(QUrl(url))
            #webbrowser.open(url)
        else:
            self.adjustSettings()

    def adjustSettings(self):
        parent = self._iface.mainWindow()
        settings = self._loadSettings()
        result = SettingsDialog(parent).askInput(settings)
        if result:
            self._saveSettings(result)
            self._targetPage = result.get(self.SETTINGS.TARGET)
            self._scaleValue = result.get(self.SETTINGS.SCALE) or 100

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
