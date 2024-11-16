import os
import subprocess


# 栅格入库
def raster2postgis(raster_path, table_name, srs='4326', schema='public', cut=None, cut_size=None, nodata=None):
    cmd = [
        'raster2pgsql',
        '-s', srs,
        '-I',
        '-C',
        '-d',
        raster_path,
        f"{schema}.{table_name}_raster",
    ]
    if cut:
        cmd.extend(['-M', '-t', f'{cut_size}x{cut_size}'])
    if nodata:
        cmd.extend(['-N', str(nodata)])

    psql_cmd = [
        'psql',
        '-d', 'carbon_forest',
        '-U', 'postgres',
        '-h', 'localhost',
        '-p', '6000',
        '-c', ' '.join(cmd)
    ]

    try:
        subprocess.run(psql_cmd, check=True, env={'PGPASSWORD': '265359'})
        print(f"Raster data from {raster_path.splice('.')[0]} has been successfully imported into table {table_name}.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


# 矢量入库
def shp2postgis(shp_path, table_name, srs='4326', schema='public'):
    cmd = [
        'ogr2ogr',
        '-f', 'PostgreSQL',
        'PG:host=localhost port=6000 user=postgres dbname=carbon_forest password=265359',
        shp_path,
        '-nln', f'{schema}.{table_name}_shp',
        '-t_srs', f'EPSG:{srs}',
        '-lco', 'GEOMETRY_NAME=geom',
        '-lco', 'FID=gid',
        '-overwrite',
    ]

    try:
        subprocess.run(cmd, check=True)
        print(f"Shapefile {shp_path.splice('.')[0]} has been successfully imported into table {table_name}.")
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")


file_list = os.listdir('D:/Desktop/invest')
shp_files = [file for file in file_list if file.endswith('.shp')]
for shp_file in shp_files:
    shp2postgis(f'D:/Desktop/invest/{shp_file}', shp_file.split('.')[0], srs='4326', schema='origin')
