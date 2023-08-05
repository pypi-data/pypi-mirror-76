from jinja2 import Environment, PackageLoader, StrictUndefined

import os

env = Environment(
    loader=PackageLoader('mapbox_location', 'templates'),
    autoescape=False,
    undefined=StrictUndefined
)


class ArrowViz(object):
    def __init__(
        self,
        access_token=None,
        azimuth_key='azimuth',
        ts_key='ts',
        center=(0, 0),
        color='red', # marker.properties['color']
        data=None,
        style='mapbox://styles/mapbox/light-v10?optimize=true'
    ):
        if access_token is None:
            access_token = os.environ.get('MAPBOX_ACCESS_TOKEN', '')
        if access_token.startswith('sk'):
            raise TokenError('Mapbox access token must be public (pk), not secret (sk). '
                             'Please sign up at https://www.mapbox.com/signup/ to get a public token. '
                             'If you already have an account, you can retreive your token at https://www.mapbox.com/account/.')
        self.access_toke = access_token
        self.center = center
        self.data = data
        self.style = style
        self.color = color
        self.azimuth_key = azimuth_key
        self.ts_key = ts_key

    def export(self, filename='mapbox.html'):
        template = env.get_template('map.html')
        html_data = template.render({
            'geojson': self.data,
            'center_lat': self.center[0],
            'center_lon': self.center[1],
            'mapbox_style': self.style,
            'mapbox_token': self.access_toke,
            'color': self.color,
            'azimuth_key': self.azimuth_key,
            'ts_key': self.ts_key
        })

        with open(filename, 'w') as f:
            f.write(html_data)
