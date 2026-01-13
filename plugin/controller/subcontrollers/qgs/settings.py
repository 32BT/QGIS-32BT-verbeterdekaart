

################################################################################
### Helperfunction
################################################################################
'''
'''
import os

def os_path_shrinkuser(path):
    home = os.path.expanduser('~')
    if home and path.startswith(home):
        path = '~'+path[len(home):]
    return path

################################################################################
### Settings
################################################################################

import sys
_MODULE = sys.modules.get(__name__.split('.')[0])
_HEADER = _MODULE.identity.HEADER
_MODULE = _MODULE.identity.MODULE

from qgis.core import QgsSettings

class Settings(QgsSettings):

    @classmethod
    def load_group(cls, key):
        with cls() as settings:
            return settings.loadGroup(key)

    @classmethod
    def save_group(cls, key, dct):
        with cls() as settings:
            settings.saveGroup(key, dct)


    def __enter__(self):
        # start with group '32bt' which will create a section [32bt]
        # (add section=self.Plugins if it needs to go in section [plugins])
        self.beginGroup(_HEADER)
        self.beginGroup(_MODULE)
        return self

    def __exit__(self, *args):
        self.endGroup()
        self.endGroup()
        # self.sync()

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
    def savePath(self, key, path):
        self.saveValue(key, os_path_shrinkuser(path))

    def loadPath(self, key):
        return os.path.expanduser(self.loadValue(key))
    ########################################################################
    def saveValue(self, key, val):
        self.setValue(key,val)

    def loadValue(self, key):
        return self.value(key, '')
    ########################################################################
