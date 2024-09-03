import requests
import rasterio
from requests.auth import HTTPBasicAuth

geoserver_url = 'http://localhost:8080/geoserver'
username = 'admin'
password = 'geoserver'
workspace = 'carbon'


class Publisher:
    def __init__(self):
        self.raster_path = None
        self.store_name = None
        self.layer_name = None
        self.style = None
        self.srs = 'EPSG:4326'

    def publish_params_set(self, obj):
        self.raster_path = obj['raster_path']
        self.store_name = obj['store_name']
        self.layer_name = obj['layer_name']
        self.style = obj['style']
        self.srs = obj['srs']

    def _calculate_extent(self):
        with rasterio.open(self.raster_path) as dataset:
            bounds = dataset.bounds
            return {
                'minx': bounds.left,
                'miny': bounds.bottom,
                'maxx': bounds.right,
                'maxy': bounds.top,
                'crs': dataset.crs.to_string()
            }

    def publish_raster(self):
        headers = {"Content-Type": "text/xml"}
        datastore_url = f'{geoserver_url}/rest/workspaces/{workspace}/datastores'
        datastore_data = f'''
        <dataStore>
            <name>{self.store_name}</name>
            <connectionParameters>
                <entry key="url">file:data/{self.raster_path}</entry>
            </connectionParameters>
        </dataStore>
        '''
        response = requests.post(datastore_url, data=datastore_data, headers=headers,
                                 auth=HTTPBasicAuth(username, password))
        if response.status_code == 201:
            print(f'Create Datastore {self.store_name} success')
        else:
            print(f'Create Datastore {self.store_name} failed', response.content)
            return

        layer_url = f'{geoserver_url}/rest/workspaces/{workspace}/coveragestores/{self.store_name}/coverages'
        layer_data = f'''
        <coverage>
          <name>{self.layer_name}</name>
          <nativeName>{self.layer_name}</nativeName>
          <title>{self.layer_name}</title>
          <srs>{self.srs}</srs>
            <nativeBoundingBox>
                <minx>{self._calculate_extent()['minx']}</minx>
                <maxx>{self._calculate_extent()['maxx']}</maxx>
                <miny>{self._calculate_extent()['miny']}</miny>
                <maxy>{self._calculate_extent()['maxy']}</maxy>
                <crs>{self.srs}</crs>
            </nativeBoundingBox>
            <latLonBoundingBox>
                <minx>{self._calculate_extent()['minx']}</minx>
                <maxx>{self._calculate_extent()['maxx']}</maxx>
                <miny>{self._calculate_extent()['miny']}</miny>
                <maxy>{self._calculate_extent()['maxy']}</maxy>
                <crs>{self.srs}</crs>
            </latLonBoundingBox>
            <defaultStyle>
                <name>{self.style}</name>
            </defaultStyle>
        </coverage>
        '''
        response = requests.post(layer_url, data=layer_data, headers=headers, auth=HTTPBasicAuth(username, password))
        if response.status_code == 201:
            print(f'Create Layer {self.layer_name} success')
        else:
            print(f'Create Layer {self.layer_name} failed', response.content)
