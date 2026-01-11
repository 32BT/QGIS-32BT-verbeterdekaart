
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

################################################################################
### Contextmenu
################################################################################
'''
'''
import sys
_MODULE = sys.modules.get(__name__.split('.')[0])

_LABELS = _MODULE.LANGUAGE.LABELS({
    "MENU_TITLE": "verbeterdekaart",
    "MENU_ITEM1": "Voorkeuren...",
    "MENU_ITEM2": "Kopieer locatie",
    "MENU_ITEM3": "Open webpagina"})

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

    def _loadSettings(self):
        return Settings.load_group(self.SETTINGS.GROUP)
    def _saveSettings(self, settings):
        Settings.save_group(self.SETTINGS.GROUP, settings)
    ########################################################################

    def __init__(self, iface, toolBar):
        self._iface = iface
        self._mapCanvas = MapCanvas(self._iface.mapCanvas())
        self._mapCanvas.connectMenuHandler(self.prepareContextMenu)

        self._menu = self._initMenu()
        action = self._menu.actions()[1]
        action.setIcon(QgsApplication.getThemeIcon("mActionEditPaste.svg"))
        action.setObjectName('vdk:copyURL')

        action = self._menu.actions()[2]
        action.setIcon(self._loadIcon())
        action.setObjectName('vdk:startBrowser')
        toolBar.addAction(action)

        settings = self._loadSettings()
        self._scaleValue = int(settings.get(self.SETTINGS.SCALE) or 100)


    def __del__(self):
        self._mapCanvas.disconnectMenuHandler(self.prepareContextMenu)
        self._mapCanvas = None

    ########################################################################
    ### Submenu
    ########################################################################

    def _initMenu(self):
        menu = QMenu(_LABELS.MENU_TITLE)
        action = menu.addAction(_LABELS.MENU_ITEM1)
        action.triggered.connect(self.adjustSettings)
        action = menu.addAction(_LABELS.MENU_ITEM2)
        action.triggered.connect(self.saveToClipboard)
        action = menu.addAction(_LABELS.MENU_ITEM3)
        action.triggered.connect(self.startBrowser)
        return menu

    def _loadIcon(self, name="vdk"):
        path = os.path.split(__file__)[0]
        path = os.path.join(path, 'icons')
        path = os.path.join(path, name+'.svg')
        return QIcon(path)

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
    def prepareContextMenu(self, menu, event):
        if len(menu.actions()) == 1:
            menu.addSeparator()
        # Add to context menu
        action = menu.addMenu(self._menu)

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
            self._scaleValue = result.get(self.SETTINGS.SCALE) or 100

    # Action 2: Copy location
    def saveToClipboard(self):
        mapPoint = None
        url = self._getURL(mapPoint)
        clipBoard = QgsApplication.clipboard()
        clipBoard.setText(url)

    # Action 3: Open verbeterdekaart in default webbrowser
    def startBrowser(self):
        mapPoint = None
        url = self._getURL(mapPoint)
        QDesktopServices.openUrl(QUrl(url))
        #webbrowser.open(url)

    ########################################################################
    ### verbeterdekaart URL
    ########################################################################
    '''
    '''
    _TARGET_CRS = QgsCoordinateReferenceSystem('EPSG:28992')

    def _getURL(self, location=None, scale=None):
        # Fetch default values if necessary
        if location is None:
            location = self._mapCanvas.getCenter()
        if scale is None:
            scale = self._mapCanvas.getScale()

        # Compensate scalefactor for webbrowser-scale differences
        scale = scale * 100. / self._scaleValue

        # Convert location & scale to verbeterkaart url
        # Zoomlevel starts at 3 for scale of 1536000,
        # each halving of scale adds one zoomlevel
        p = self._mapCanvas.convertMapPoint(location, self._TARGET_CRS)
        s = 3. + math.log2(1536000./scale)

        # Create url with parameters
        url = 'https://verbeterdekaart.nl/#?'
        url += '&'.join((
            'geometry.x={:.03f}'.format(p.x()),
            'geometry.y={:.03f}'.format(p.y()),
            'zoomlevel={:.03f}'.format(s)))
        return url


################################################################################
