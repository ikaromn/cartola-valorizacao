import json
import requests

from cartola_mn import settings
from .cartola_resource_mapping import cartola_mapping


class Cartola:
    def _get_header(self):
        return {
            'x-glb-token': settings.CARTOLA_TOKEN,
        }

    def _get_url(self, resource_name, **kwargs):
        resource = cartola_mapping[resource_name]

        if '{' in resource:
            resource = resource.format(**kwargs)

        return f'http://api.cartolafc.globo.com/{resource}'

    def make_request(self, name, **kwargs):
        header = self._get_header()
        response = requests.get(self._get_url(name, **kwargs), headers=header)
        return json.loads(response.content)
