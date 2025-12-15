
import math, webbrowser

from qgis.gui import *
from qgis.core import *
from qgis.PyQt.QtCore import *
from qgis.PyQt.QtWidgets import *
from qgis.PyQt.QtGui import *

from .settings import Settings
from .mapcanvas import MapCanvas

################################################################################
### Controller
################################################################################

class Controller:

    def __init__(self, iface):
        self._iface = iface
        self._mapCanvas = MapCanvas(self._iface.mapCanvas())
        self._mapCanvas.connectMenuHandler(self.prepareContextMenu)

    def __del__(self):
        self._mapCanvas.disconnectMenuHandler(self.prepareContextMenu)
        self._mapCanvas = None

    ########################################################################
    ### Contextmenu preparation
    ########################################################################
    '''
    The process is started by right-clicking the mapCanvas. This presents
    a contextmenu. Just before the contextmenu will be shown, we will receive
    a signal: contextMenuAboutToShow. That signal is handled here.

    This will add a menuitem "verbeterdekaart" with 3 submenus.
    '''
    _MENU_TITLE = "verbeterdekaart"
    _PRF_ACTION_NAME = "Voorkeuren..."
    _URL_ACTION_NAME = "Kopieer locatie"
    _WEB_ACTION_NAME = "Melding aanmaken..."

    def prepareContextMenu(self, menu: QMenu, event: QgsMapMouseEvent):
        # Translate mousePoint to mapPoint
        mapPoint = self._mapCanvas.getMapPointForEventPosition(event.pos())

        # Add context menu
        menu = menu.addMenu(self._MENU_TITLE)
        action = menu.addAction(self._PRF_ACTION_NAME)
        action.triggered.connect(self.adjustSettings)
        action = menu.addAction(self._URL_ACTION_NAME)
        action.triggered.connect(lambda *args: self.saveToClipboard(mapPoint))
        action = menu.addAction(self._WEB_ACTION_NAME)
        action.triggered.connect(lambda *args: self.startBrowser(mapPoint))

    ########################################################################
    ### Contextmenu actions
    ########################################################################
    '''
    If the user actually selects one of the menuitems, the corresponding
    action will be triggered.
        Action 0 will start a dialog to set preferences, specifically
            a compensation for verbeterdekaart scaling.
        Action 1 will copy the current maplocation & scale in
            verbeterdekaart-compatible format to the clipboard.
        Action 2 will open the current maplocation & scale in
            the default webbrowser.
    '''
    # Action 0: adjust preferences
    def adjustSettings(self):
        parent = self._iface.mainWindow()
        Settings.adjustSettings(parent)

    # Action 1: Copy location
    def saveToClipboard(self, mapPoint):
        url = self._getURL(mapPoint)
        clipBoard = QgsApplication.clipboard()
        clipBoard.setText(url)

    # Action 2: Open verbeterdekaart in default webbrowser
    def startBrowser(self, mapPoint):
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
        scale = Settings.compensateScale(scale)

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

    ########################################################################

################################################################################
