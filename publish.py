import requests
import rasterio
from pyproj import Transformer
from requests.auth import HTTPBasicAuth

geoserver_url = 'http://localhost:8080/geoserver'
username = 'admin'
password = 'geoserver'


class Publisher:
    def __init__(self):
        self.data_path = None
        self.data_type = None
        self.workspace = None
        self.store_name = None
        self.layer_name = None
        self.style = None
        self.srs = 'EPSG:4326'

    def publish_params_set(self, obj):
        self.data_path = obj['data_path']
        self.data_type = obj['data_type']
        self.workspace = obj['workspace']
        self.store_name = obj['store_name']
        self.layer_name = obj['layer_name']
        self.style = obj['style']
        self.srs = obj['srs']

    def _calculate_extent(self):
        with rasterio.open(self.data_path) as dataset:
            bounds = dataset.bounds
            transformer = Transformer.from_crs(dataset.crs, self.srs, always_xy=True)
            minx, miny = transformer.transform(bounds.left, bounds.bottom)
            maxx, maxy = transformer.transform(bounds.right, bounds.top)
            return {
                'minx': minx,
                'miny': miny,
                'maxx': maxx,
                'maxy': maxy,
                'crs': self.srs
            }

    def publish(self):
        url, headers = None, None
        if self.data_type == 'GeoTIFF':
            url = f'{geoserver_url}/rest/workspaces/{self.workspace}/coveragestores/{self.store_name}/file.geotiff'
            headers = {'Content-type': 'image/tiff'}
        if self.data_type == 'Shapefile':
            url = f'{geoserver_url}/rest/workspaces/{self.workspace}/datastores/{self.store_name}/file.shp'
            headers = {'Content-type': 'application/zip'}
        data_file = open(self.data_path, 'rb')
        response = requests.put(url, auth=HTTPBasicAuth(username, password), data=data_file.read(), headers=headers)
        if response.status_code == 201:
            print(f'Create Datastore {self.store_name} success')
        else:
            print(f'Create Datastore {self.store_name} failed', response.content)
            return

        extent = self._calculate_extent()
        headers = {'Content-type': 'application/xml'}
        layer_url = f'{geoserver_url}/rest/workspaces/{self.workspace}/coveragestores/{self.store_name}/coverages/{self.layer_name}.xml'
        coverage_xml = f'''
        <coverage>
          <name>{self.layer_name}</name>
          <nativeName>{self.layer_name}</nativeName>
          <title>{self.layer_name}</title>
          <srs>{self.srs}</srs>
            <nativeBoundingBox>
                <minx>{extent['minx']}</minx>
                <maxx>{extent['maxx']}</maxx>
                <miny>{extent['miny']}</miny>
                <maxy>{extent['maxy']}</maxy>
                <crs>{self.srs}</crs>
            </nativeBoundingBox>
            <latLonBoundingBox>
                <minx>{extent['minx']}</minx>
                <maxx>{extent['maxx']}</maxx>
                <miny>{extent['miny']}</miny>
                <maxy>{extent['maxy']}</maxy>
            </latLonBoundingBox>
            <defaultStyle>
                <name>{self.style}</name>
            </defaultStyle>
        </coverage>
        '''
        response = requests.put(layer_url, data=coverage_xml, headers=headers, auth=HTTPBasicAuth(username, password))
        if response.status_code == 201 & 200:
            print(f'Create Layer {self.layer_name} success')
        else:
            print(f'Create Layer {self.layer_name} failed', response.content)
