
'''
Need overal designstrategy for new OGC API endpoints

The Kadaster OGC API endpoints support filtering, but
QGIS only forwards datetime to the server.

We would like to implement QGIS expression filter in WFS, since
that plays well with the layerproperties dialog, but
that probably does not work with the OGC API.
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

