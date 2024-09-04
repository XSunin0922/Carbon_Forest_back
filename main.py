import arcpy
from model.simplify_raster import *
from publish import Publisher

arcpy.env.workspace = r"D:\Desktop\cfb"
arcpy.env.overwriteOutput = True

input_raster = "zsj_lulc_10.tif"
resam = resample_raster(input_raster, "z_l_10_resample.tif", 2000)
maj = majority_filter(resam, "z_l_10_resample_maj11.tif", 11)

params = {
    'data_path': 'z_l_10_resample_maj11.tif',
    'data_type': 'GeoTIFF',
    'workspace': 'carbon',
    'store_name': 'z_l_10_resample_maj11',
    'layer_name': 'z_l_10_resample_maj11',
    'style': 'lulc_image',
    'srs': 'EPSG:4326'
}
publisher = Publisher()
publisher.publish_params_set(params)
publisher.publish()
