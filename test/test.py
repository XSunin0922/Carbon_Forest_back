from model.tools import *
from publish import Publisher

# simplify_params = {
#     'input_raster': 'zsj_lulc_10.tif',
#     'output_raster': 'z_l_10_simplify.tif',
#     'resample_cell_size': 2000,
#     'filter_cell_size': 11
# }
# simplify = Simplify()
# simplify.simplify_params_set(simplify_params)
# simplify.simplify()


# publish_params = {
#     'data_path': 'z_l_10_resample_maj11.tif',
#     'data_type': 'GeoTIFF',
#     'workspace': 'carbon',
#     'store_name': 'z_l_10_resample_maj11',
#     'layer_name': 'z_l_10_resample_maj11',
#     'style': 'lulc_image',
#     'srs': 'EPSG:4326'
# }
# publisher = Publisher()
# publisher.publish_params_set(params)
# publisher.publish()


# neighbor_recognition_params = {
#     'input_raster': 'z_l_10_simplify.tif',
#     'output_feature': "neighbor_extent.shp",
#     'forest_index': 2,
# }
# neighborRecognition = NeighborRecognition()
# neighborRecognition.neighbor_recognition_params_set(neighbor_recognition_params)
# neighborRecognition.neighbor_recognition()


edge_effect_measure_params = {
    'carbon_raster': 'china10_carbon84.tif',
    'neighbor_extent': 'neighbor_extent.shp',
    'output_table': 'edge_effect_measure.xlsx',
    'distance_class': 5,
    'edge_distance': 50,  # km
}
edgeEffectMeasure = EdgeEffectMeasure()
edgeEffectMeasure.edge_effect_measure_params_set(edge_effect_measure_params)
edgeEffectMeasure.edge_effect_measure()

