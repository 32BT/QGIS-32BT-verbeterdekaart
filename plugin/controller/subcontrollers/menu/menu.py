

from qgis.PyQt.QtWidgets import QMenu

'''
Menu items behoeven geen vertaling.
'''
class MENU:
    TITLE = "verbeterdekaart"
    class ITEM:
        BAG = "BAG Viewer (BAG)"
        BGT = "Verbeter de Kaart (BGT/BRT/3DB)"
        AERO = "Verbeter de Luchtvaartkaart (AERO)"
        SETTINGS = "Voorkeuren..."

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
