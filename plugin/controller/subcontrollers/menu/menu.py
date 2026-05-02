

from qgis.PyQt.QtWidgets import QMenu

###############################################################################
### Labels
###############################################################################

_LABELS = {
    "CANVASMENU": {
        "TITLE": "verbeterdekaart",
        "PREFS": "Voorkeuren..."
    }
}

import sys
_MODULE = sys.modules.get(__name__.split('.')[0])
_LABELS = _MODULE.LANGUAGE.LABELS(_LABELS)

###############################################################################
### Menu
###############################################################################

class MENU:
    TITLE = "verbeterdekaart"
    class ITEM:
        BAG = "BAG Viewer (BAG)"
        BGT = "Verbeter de Kaart (BGT/BRT/3DB)"
        AERO = "Verbeter de Luchtvaartkaart (AERO)"
        SETTINGS = _LABELS.CANVASMENU.PREFS

class TARGET:
    class PAGE:
        BAG = 'BAG'
        BGT = 'BGT'
        AERO = 'AERO'
        LIST = (BAG, BGT, AERO)

class TargetMenu(QMenu):
    def __init__(self):
        super().__init__(MENU.TITLE)
        action = self.addAction(MENU.ITEM.BAG)
        action._targetPage = TARGET.PAGE.BAG
        action = self.addAction(MENU.ITEM.BGT)
        action._targetPage = TARGET.PAGE.BGT
        action = self.addAction(MENU.ITEM.AERO)
        action._targetPage = TARGET.PAGE.AERO
        self.addSeparator()
        action = self.addAction(MENU.ITEM.SETTINGS)
        action._targetPage = "Settings"

    def prepare(self, focusMode="Ad hoc"):
        self.setDefaultAction(None)
        for a in self.actions():
            if getattr(a, '_targetPage', None) == focusMode:
                self.setDefaultAction(a)
        return self

    def findModeTitle(self, mode):
        try:
            index = TARGET.PAGE.LIST.index(mode)
            action = self.actions()[index]
            return action.text()
        except Exception:
            return ""
