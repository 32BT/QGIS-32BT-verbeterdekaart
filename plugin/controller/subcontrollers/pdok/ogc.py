
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
    SERVICES = {
        "BAG": "https://api.pdok.nl/kadaster/bag-terugmeldingen/ogc/v1",
        "BGT": "https://api.pdok.nl/kadaster/bgt-terugmeldingen/ogc/v1",
        "BRT": "https://api.pdok.nl/kadaster/brt-terugmeldingen/ogc/v1",
        "3DB": "https://api.pdok.nl/kadaster/3d-basisvoorziening-terugmeldingen/ogc/v1",
        "AERO": "https://api.pdok.nl/defensie/luchtvaartobstakels-terugmeldingen/ogc/v1" }
    TYPENAMES = {
        "3DB": "kad3dbasisvoorziening" }

    class DEFAULT:
        class CRS:
            NAME = "EPSG:28992"
            LINK = "http://www.opengis.net/def/crs/EPSG/0/28992"

    ################################################################

    @classmethod
    def get_itemtype(cls, service_id):
        itemtype = cls.TYPENAMES.get(service_id)
        return (itemtype or service_id.lower()) +'terugmeldingen'

    ########################################################################

    @classmethod
    def get_url(cls, service_id, owner_id=None):
        url = cls.SERVICES.get(service_id)
        prm = []
        if owner_id:
            prm += ["bronhoudercode="+owner_id]
        return url+'?'+'&'.join(prm)

    @classmethod
    def _crs_as_prm(cls, service_id=None):
        crs = "crs="+cls.DEFAULT.CRS.LINK
        crs = crs.replace(":", "%3A")
        crs = crs.replace("/", "%2F")
        return crs

