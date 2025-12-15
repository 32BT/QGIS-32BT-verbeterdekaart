
################################################################################
### classFactory
################################################################################

def classFactory(iface):
    from .controller import Controller

    class Plugin:
        def __init__(self, iface):
            self._iface = iface

        def initGui(self):
            self._controller = Controller(self._iface)

        def unload(self):
            self._controller = None

    return Plugin(iface)

################################################################################
