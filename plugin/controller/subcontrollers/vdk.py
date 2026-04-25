

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


###############################################################################
### Voorkeuren
###############################################################################
class SETTINGS(dict):
    GROUP = 'voorkeuren'
    SCALE = 'schalingspercentage'

    class TARGET:
        class MODE:
            KEY = 'modus'
            ADHOC = 'Ad hoc'
        class PAGE:
            KEY = 'doel'
            BAG = 'BAG'
            BGT = 'BGT'
            AERO = 'AERO'
            LIST = (BAG, BGT, AERO)

    def get_targetMode(self):
        return self.get(self.TARGET.MODE.KEY) or self.TARGET.MODE.ADHOC
    def get_targetPage(self):
        return self.get(self.TARGET.PAGE.KEY) or self.TARGET.PAGE.BGT
    def get_scaleValue(self):
        return int(self.get(SETTINGS.SCALE) or 100)

    def set_targetMode(self, value):
        self[self.TARGET.MODE.KEY] = value
        if value in self.TARGET.PAGE.LIST:
            self[self.TARGET.PAGE.KEY] = value

    def set_scaleValue(self, value):
        self[SETTINGS.SCALE] = int(value)

###############################################################################
### VDKController
###############################################################################

class Controller:

    def __init__(self, iface, toolBar):
        self._iface = iface

        self._buttonMenu = TargetMenu()
        self._buttonMenu.setObjectName("vdk:buttonMenu")
        self._menuButton = MenuButton(toolBar, loadIcon("vdk"), self._buttonMenu)
        self._menuButton.instantActionTriggered.connect(self.instantActionTriggered)
        self._menuButton.delayedActionTriggered.connect(self.delayedActionTriggered)

        self._canvasMenu = TargetMenu()
        self._canvasMenu.setObjectName("vdk:canvasMenu")
        self._canvasMenu.triggered.connect(self.instantActionTriggered)

        self._mapCanvas = MapCanvas(self._iface.mapCanvas())
        self._mapCanvas.connectMenuHandler(self.contextMenuAboutToShow)
        self._mapCanvas.connectExtentHandler(self.updateButtons)

        self.loadSettings()


    def __del__(self):
        self._mapCanvas.disconnectExtentHandler(self.updateButtons)
        self._mapCanvas.disconnectMenuHandler(self.contextMenuAboutToShow)
        self._mapCanvas = None

    #######################################################################
    '''
    Verbeterdekaart is only meaningful within countrybounds.
    If the visible extent does not overlap the country extent, then the tool-
    button will be disabled, and the canvasmenu will not be attached.
    '''
    def isDomainVisible(self):
        crs = QgsCoordinateReferenceSystem('EPSG:28992')
        mapR = self._mapCanvas.visibleExtent(crs)
        dstR = QgsRectangle(0, 300000, 300000, 630000)
        return mapR.intersects(dstR)

    '''
    Button updates are triggered by mapCanvas extentsChanged signal.
    '''
    def updateButtons(self):
        enable = self.isDomainVisible()
        self._menuButton.setEnabled(enable)

    #######################################################################
    ### Contextmenu preparation
    #######################################################################
    '''
    Right-clicking the mapCanvas will present a contextmenu.
    The mapcanvas will emit a contextMenuAboutToShow-signal first.
    This allows us to attach our menu to the contextmenu.

    This must be done each time the signal is triggered.
    '''
    def contextMenuAboutToShow(self, contextMenu, event):
        if self.isDomainVisible():
            if len(contextMenu.actions()) == 1:
                contextMenu.addSeparator()
            # Add our menu to context menu
            action = contextMenu.addMenu(self._canvasMenu)

    #######################################################################
    ### Menu actions
    #######################################################################
    '''
    Actions will either be:
        instant actions OR delayed actions, and
        a verbeterdekaart target OR the settings option.
    A delayed action results from a delayed popup when in focusmode.
    A delayed action in the targets category, is a focusmodeswitch.

                |  BAG/BGT/AERO  |  Settings
        -------------------------------------------------
        instant |  open webpage  |  open settingsdialog
        delayed |  switch focus  |  open settingsdialog
    '''

    def delayedActionTriggered(self, action=None):
        target = getattr(action, '_targetPage', None)
        if target in PDOK.VDK.TARGET.LIST:
            self.setTargetPage(target)
        else:
            self.adjustSettings()

    def instantActionTriggered(self, action=None):
        target = getattr(action, '_targetPage', None)
        if target in PDOK.VDK.TARGET.LIST:
            self.startBrowser(target)
        else:
            self.adjustSettings()

    #######################################################################
    ### Settings
    #######################################################################

    def _loadSettings(self):
        return Settings.load_group(SETTINGS.GROUP)

    def _saveSettings(self, settings):
        Settings.save_group(SETTINGS.GROUP, settings)

    def adjustSettings(self):
        parent = self._iface.mainWindow()
        settings = self._settings
        settings = SettingsDialog(parent).askInput(settings)
        if settings:
            self._saveSettings(settings)
            self.loadSettings()

    def loadSettings(self):
        settings = self._loadSettings()
        settings = SETTINGS(settings or {})
        self._settings = settings
        self._scaleValue = settings.get_scaleValue()
        self._targetPage = settings.get_targetPage()
        self._targetMode = settings.get_targetMode()
        self._menuButton.setFocusMode(self._targetMode)

    #######################################################################

    def setTargetPage(self, targetPage):
        settings = self._settings
        if self._targetMode != targetPage:
            self._targetMode = targetPage
            self._targetPage = targetPage
            settings[SETTINGS.TARGET.MODE.KEY] = targetPage
            settings[SETTINGS.TARGET.PAGE.KEY] = targetPage
            self._saveSettings(settings)
        self._menuButton.setFocusMode(targetPage)

    def startBrowser(self, targetPage):
        url = self._getURL(targetPage)
        QDesktopServices.openUrl(QUrl(url))
        #webbrowser.open(url)

    #######################################################################
    ### verbeterdekaart URL
    #######################################################################
    '''
    '''
    def _getURL(self, service='BGT', point=None, scale=None):
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

###############################################################################
