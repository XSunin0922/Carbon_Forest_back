import arcpy
from arcpy.sa import *


# 众数滤波
def majority_filter(input_raster, output_raster, cell_size):
    neighborhood = NbrRectangle(cell_size, cell_size, "CELL")
    re = FocalStatistics(input_raster, neighborhood, "MAJORITY")
    if output_raster:
        re.save(output_raster)
    return re


# 重采样
def resample_raster(input_raster, output_raster, cell_size):
    arcpy.management.Resample(input_raster, output_raster, cell_size, "MAJORITY")
    return output_raster
