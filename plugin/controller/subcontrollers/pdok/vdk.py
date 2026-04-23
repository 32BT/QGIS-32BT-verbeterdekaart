

import math

################################################################################
### TMS.VDK
################################################################################

class VDK:
    class URL:
        BAG = "https://bagviewer.kadaster.nl/?theme=Luchtfoto%27s&"
        BGT = "https://www.verbeterdekaart.nl/#?"
        AERO = "https://www.verbeterdeluchtvaartkaart.nl/#/kaart?"

    class CRS:
        BGT = 'EPSG:28992'


    @classmethod
    def get_service_crs(cls, service='BGT'):
        return cls._get_crs(service)

    @classmethod
    def get_service_url(cls, service, point, scale):
        url = cls._get_url(service)
        prm = cls._get_prm(point, scale)
        return url+prm

    @classmethod
    def _get_crs(cls, service='BGT'):
        return getattr(cls.CRS, service, cls.CRS.BGT)

    @classmethod
    def _get_url(cls, service='BGT'):
        return getattr(cls.URL, service, cls.URL.BGT)

    @staticmethod
    def _get_prm(location=None, scale=None):
        # Convert location & scale to verbeterkaart url
        # Zoomlevel starts at 3 for scale of 1536000,
        # each halving of scale adds one zoomlevel
        p = location
        s = 3. + math.log2(1536000./scale)

        # Create url parameters
        return '&'.join((
            'geometry.x={:.03f}'.format(p.x()),
            'geometry.y={:.03f}'.format(p.y()),
            'zoomlevel={:.03f}'.format(s)))
