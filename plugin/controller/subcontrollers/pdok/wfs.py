


################################################################################
### TMS.WFS
################################################################################

class WFS:
    _URLS = {
        "BAG": "https://service.pdok.nl/lv/bag/terugmeldingen/wfs/v1_0",
        "BGT": "https://service.pdok.nl/lv/bgt/terugmeldingen/wfs/v1_0",
        "BRT": "https://service.pdok.nl/brt/terugmeldingen/wfs/v1_0",
        "3DB": "https://service.pdok.nl/kadaster/basisvoorziening-3d/terugmeldingen/wfs/v1_0",
        "AERO": "https://service.pdok.nl/defensie/luchtvaartobstakels/terugmeldingen/wfs/v1_0" }

    _PRMS = dict(
        service="WFS",
        version="2.0.0",
        request="getfeature",
        typeNames="*terugmeldingen")

    ################################################################

    _FLTR = ''.join((
        '<Filter>',
        #'<PropertyIsLike wildCard="*" singleChar="?" escapeChar="%">',
        '<PropertyIsLike wildCard="%" singleChar="_" escapeChar="\\">',
        '<PropertyName>bronhoudercode</PropertyName>',
        '<Literal>{}</Literal>',
        '</PropertyIsLike>',
        '</Filter>'))

    @classmethod
    def get_filter(cls, owner_id):
        return cls._FLTR.format(owner_id)

    ################################################################

    _TYPENAMES = {
        "3DB": "kad3dbasisvoorziening" }

    @classmethod
    def get_itemtype(cls, service_id):
        itemtype = cls._TYPENAMES.get(service_id)
        return (itemtype or service_id.lower()) +'terugmeldingen'

    ########################################################################

    @classmethod
    def get_url(cls, service_id, owner_id=None):
        url = cls._URLS.get(service_id)
        prm = ["service=WFS"]
        prm += ["version=2.0.0"]
        prm += ["request=GetFeature"]
        prm += ["typename="+cls.get_itemtype(service_id)]
        if owner_id:
            prm += ["filter="+cls.get_filter(owner_id)]
        return url+'?'+'&'.join(prm)

