

from qgis.core import QgsApplication


################################################################################
### Labels
################################################################################
'''
Given an instance of LABELS:

    _LABELS = LABELS(...)

Then following will all return the same result:

    _LABELS.CUSTOM_LABEL
    _LABELS("CUSTOM_LABEL")
    _LABELS["CUSTOM_LABEL"]
    _LABELS.get("CUSTOM_LABEL")
'''
import os, json

class LABELS(dict):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        super().update(self.loadLanguage() or {})

    def __call__(self, k):
        return self.get(k)

    def __getattr__(self, k):
        return self.get(k)

    def __getitem__(self, k):
        return self.get(k)

    def get(self, k):
        v = super().get(k)
        if isinstance(v, list):
            v = '\n'.join(v)
        return v or k or ""

    @classmethod
    def loadLanguage(cls, lang=None):
        lang = lang or QgsApplication.instance().locale()
        path = os.path.dirname(__file__)
        path = os.path.join(path, str(lang).lower()+'.json')
        if os.path.exists(path):
            with open(path, encoding='utf-8') as f:
                return json.loads(f.read())
