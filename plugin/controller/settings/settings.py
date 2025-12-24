################################################################################
### Settings
################################################################################

from qgis.core import QgsSettings

class Settings(QgsSettings):

    def __init__(self, pluginName):
        super().__init__()
        self._pluginName = pluginName

    def __enter__(self):
        # start with group '32bt' which will create a section [32bt]
        # (add section=self.Plugins if it needs to go in section [plugins])
        self.beginGroup('32bt')
        self.beginGroup(self._pluginName)
        return self

    def __exit__(self, *args):
        self.endGroup()
        self.endGroup()
        self.sync()

    ########################################################################
    # save dictionary k,v pairs under groupname key
    def saveGroup(self, key, dct):
        self.remove(key)
        self.beginGroup(key)
        try:
            self.saveGroupValues(dct)
        finally:
            self.endGroup()

    def loadGroup(self, key):
        self.beginGroup(key)
        try:
            return self.loadGroupValues()
        finally:
            self.endGroup()

    ########################################################################

    def saveGroupValues(self, dct):
        for key,val in dct.items():
            if isinstance(val, dict):
                self.saveGroup(key, val)
            else:
                self.saveValue(key, val)

    def loadGroupValues(self):
        D = {}
        for key in self.childKeys():
            D[key] = self.loadValue(key)
        for key in self.childGroups():
            D[key] = self.loadGroup(key)
        return D

    ########################################################################
    def saveValue(self, key, val):
        self.setValue(key,val)

    def loadValue(self, key):
        return self.value(key, '')
    ########################################################################
