

'''
The Kadaster OGC API endpoints only support rudimentary filtering using
closed url params (meaning: no wildcards). The endpoints do not support
ogc filters currently, nor datetime forwarding.

QGIS forwards only datetime to the server for ogc endpoints.

'''

################################################################################
### TMS.OGC
################################################################################

class OGC:
    class ENDPOINT:
        DOM = "https://api.pdok.nl"
        URL = {
        "BAG": DOM+"/kadaster/bag-terugmeldingen/ogc/v1",
        "BGT": DOM+"/kadaster/bgt-terugmeldingen/ogc/v1",
        "BRT": DOM+"/kadaster/brt-terugmeldingen/ogc/v1",
        "3DB": DOM+"/kadaster/3d-basisvoorziening-terugmeldingen/ogc/v1",
        "AERO": DOM+"/defensie/luchtvaartobstakels-terugmeldingen/ogc/v1" }

        def __new__(cls, service_id):
            return cls.URL.get(service_id)

    class ITEMTYPE:
        PREFIX = {
            "3DB": "kad3dbasisvoorziening" }

        def __new__(cls, service_id):
            prefix = cls.PREFIX.get(service_id) or service_id.lower()
            return prefix+"terugmeldingen"

    class DEFAULT:
        class CRS:
            NAME = "EPSG:28992"
            LINK = "http://www.opengis.net/def/crs/EPSG/0/28992"

    ########################################################################

    class FILTER:
        KEYS = (
            "bronhoudercode",
            "bronhoudernaam",
            "meldingsnummer_volledig",
            "objecttype",
            "status")

        def __new__(cls, key, val):
            return f"{key}={val}"



