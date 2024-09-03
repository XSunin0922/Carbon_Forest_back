import arcpy
from model.simplify_raster import *
from publish import Publisher

arcpy.env.workspace = r"D:\Desktop\cfb"
arcpy.env.overwriteOutput = True

input_raster = "zsj_lulc_10.tif"
output_raster = "z_l_10_maj21.tif"

maj = majority_filter(input_raster, output_raster, 21)
resample_raster(maj, "z_l_10_maj21_resample.tif", 2000)

params = {
    'raster_path': 'z_l_10_maj21_resample.tif',
    'store_name': 'z_l_10_maj21_resample',
    'layer_name': 'z_l_10_maj21_resample',
    'srs': 'EPSG:4326'
}
publisher = Publisher()
publisher.publish_params_set(params)
publisher.publish_raster()