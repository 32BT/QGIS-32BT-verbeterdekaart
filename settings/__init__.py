

from .dialog import Dialog as SettingsDialog
from .settings import Settings as PluginSettings


class Settings:

    ########################################################################
    PLUGIN_NAME = "verbeterdekaart"

    @classmethod
    def load(cls):
        with PluginSettings(cls.PLUGIN_NAME) as settings:
            return settings.loadGroup("voorkeuren")

    @classmethod
    def save(cls, prefs):
        with PluginSettings(cls.PLUGIN_NAME) as settings:
            return settings.saveGroup("voorkeuren", prefs)

    ########################################################################
    SCALE_KEY = "schalingspercentage"

    @classmethod
    def loadScale(cls):
        prefs = cls.load()
        value = prefs.get(cls.SCALE_KEY, 100)
        return int(value)

    @classmethod
    def saveScale(cls, value):
        prefs = { cls.SCALE_KEY: value }
        cls.save(prefs)
        return value

    ########################################################################
    '''
    QGIS uses screen resolution for scale representation.
    DOM only provides 96dpi as screenresolution, so the vdk scale may differ
    relative to the qgis representation. Additional factors affect the scale
    representation including the possibility of multiple screens.

    So, the user can set a scalefactor that allows the verbeterdekaart
    representation to match the current QGIS representation.

    A guestimate can be retreived from the QGIS python console via:
        QgsApplication.instance().primaryScreen().physicalDotsPerInch() / 96
    '''
    @classmethod
    def compensateScale(cls, s):
        return s * 100. / cls.loadScale()

    @classmethod
    def adjustSettings(cls, parent):
        value = cls.loadScale()
        value = SettingsDialog(parent).askScale(value)
        if value: return cls.saveScale(value)


