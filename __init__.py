
class IDENTITY:
    from .identity import PREFIX

def classFactory(iface):
    from .plugin import Plugin
    return Plugin(iface)
