

################################################################################
### TMS.WFS
################################################################################

class WFS:
    class ENDPOINT:
        DOM = "https://service.pdok.nl"
        URL = {
            "BAG": DOM+"/kadaster/bag-terugmeldingen/wfs/v1_0",
            "BGT": DOM+"/kadaster/bgt-terugmeldingen/wfs/v1_0",
            "BRT": DOM+"/kadaster/brt-terugmeldingen/wfs/v1_0",
            "3DB": DOM+"/kadaster/3d-basisvoorziening-terugmeldingen/wfs/v1_0",
            "AERO": DOM+"/defensie/luchtvaartobstakels/terugmeldingen/wfs/v1_0" }

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
        TMP = ''.join((
        '<Filter>',
        #'<PropertyIsLike wildCard="*" singleChar="?" escapeChar="%">',
        '<PropertyIsLike wildCard="%" singleChar="_" escapeChar="\\">',
        '<PropertyName>{}</PropertyName>',
        '<Literal>{}</Literal>',
        '</PropertyIsLike>',
        '</Filter>'))

        def __new__(cls, key, val):
            return TMP.format(key, val)

    ########################################################################

    @classmethod
    def get_url(cls, service_id, owner_id=None):
        url = cls.ENDPOINT(service_id)
        prm = dict(
            service="WFS",
            version="2.0.0",
            request="getfeature",
            typename=cls.ITEMTYPE(service_id))
        if owner_id:
            prm["filter"] = cls.FILTER("bronhoudercode", owner_id)
        prm = [f"{k}={v}" for k,v in prm.items()]
        return url+'?'+'&'.join(prm)

