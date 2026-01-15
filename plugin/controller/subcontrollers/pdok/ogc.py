
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
    SERVICE = {
        "BAG": "https://api.pdok.nl/kadaster/bag-terugmeldingen/ogc/v1",
        "BGT": "https://api.pdok.nl/kadaster/bgt-terugmeldingen/ogc/v1",
        "BRT": "https://api.pdok.nl/kadaster/brt-terugmeldingen/ogc/v1",
        "3DB": "https://api.pdok.nl/kadaster/3d-basisvoorziening-terugmeldingen/ogc/v1",
        "AERO": "https://api.pdok.nl/defensie/luchtvaartobstakels-terugmeldingen/ogc/v1" }
    TYPENAMES = {
        "3DB": "kad3dbasisvoorziening" }

    ################################################################

    @classmethod
    def get_itemtype(cls, service_id):
        itemtype = cls.SERVICE.TYPENAMES.get(service_id)
        return (itemtype or service_id.lower()) +'terugmeldingen'

    ########################################################################

    @classmethod
    def get_url(cls, service_id, owner_id=None):
        url = cls.SERVICE.get(service_id)
        # crs=http://www.opengis.net/def/crs/EPSG/0/28992
        prm = []
        if owner_id:
            prm += ["bronhoudercode="+owner_id]
        return url+'?'+'&'.join(prm)


